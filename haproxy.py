import time
from pygtail import Pygtail

from lepsius import bucketize, group_by, apdex, grok_parser
from lepsius.carbon import CarbonClient


def forever_tail(path, offset):
    while True:
        for line in Pygtail(path, offset):
            if type(line) == bytes:
                yield line.decode('utf8', 'replace')
            else:
                yield line
        time.sleep(10)

MIN = "haproxy.backends.{backend}.time_backend_response.min"
MAX = "haproxy.backends.{backend}.time_backend_response.max"
MEDIAN = "haproxy.backends.{backend}.time_backend_response.median"
APDEX = "haproxy.apdex.backends.{backend}.apdex"
HITS = "haproxy.apdex.backends.{backend}.hits"
STATUS = "haproxy.http_status.{service}.{status}"

if __name__ == '__main__':
    import sys
    import os
    import os.path

    carbon = CarbonClient(os.getenv("CARBON_HOST", "localhost"))

    def oups(line):
        print("OUPS", line)

    if len(sys.argv) > 1:
        offset = os.getenv("OFFSET_FOLDER", None)
        if offset:
            full = os.path.abspath(sys.argv[1]).replace('/', '-')
            offset = "%s/%s.offset" % (offset, full)
        source = forever_tail(sys.argv[1], offset)
    else:
        source = sys.stdin

    lines = grok_parser("%{HAPROXYHTTP}", source,
                        cb_oups=oups,
                        date_key="accept_date",
                        date_format="%d/%b/%Y:%H:%M:%S.%f")
    for ts, bucket in bucketize(lines):
        points = [dict(measurement="latency",
                       tags=dict(backend=v['backend_name'],
                                 status_code=v['http_status_code']),
                       # time=ts,
                       fields=dict(latency=int(v.get('time_backend_response',
                                                     0)))
                       )
                  for v in bucket]
        print(points)

        backends = group_by(bucket, 'backend_name')

        for backend, values in backends.items():
            latencies = [int(v['time_backend_response']) for v in values
                         if v['http_status_code'] in ['200', '201']]
            a, hits = apdex(latencies, 3)
            print(backend, latencies, a)
            assert a is None or a <= 1.0
            if a is not None:
                carbon.send(APDEX.format(backend=backend), int(a * 100), ts)
                carbon.send(HITS.format(backend=backend), hits, ts)
            for status, values in group_by(values, 'http_status_code').items():
                carbon.send(STATUS.format(service=backend, status=status),
                            len(values), ts)
                print(backend, status, len(values))
            v = [int(v['time_backend_response']) for v in values
                 if v['time_backend_response'] != '-1']
            print("time_backend_response", v)
            if len(v) > 0:
                v.sort()
                carbon.send(MIN.format(backend=backend), v[0], ts)
                carbon.send(MAX.format(backend=backend), v[-1], ts)
                carbon.send(MEDIAN.format(backend=backend),
                            v[int(len(v) / 2)], ts)
