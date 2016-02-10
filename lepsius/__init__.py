from collections import defaultdict
from datetime import datetime
import time

from pygrok import grok_match
from pygtail import Pygtail

"""
Use something like this:

import sys
from pygtail import Pygtail

lines = grok_parser("%{HAPROXYHTTP}", Pygtail(sys.argv[1]),
                    date_key="accept_date",
                    date_format="%d/%b/%Y:%H:%M:%S.%f")
for ts, bucket in bucketize(lines):
    # One bucket per minute
    backends = group_by(bucket, 'backend_name')

    for backend, values in backends.items():
        # Now, you can compute group by backend

"""


def forever_tail(path):
    while True:
        for line in Pygtail(path):
            yield line
        time.sleep(10)


def grok_parser(pattern, lines, cb_oups=None, date_key=None, date_format=None):
    for line in lines:
        m = grok_match(line, pattern)
        if m is None:
            if cb_oups is not None:
                cb_oups(line)
            continue
        if None not in {date_key, date_format}:
            ts = datetime.strptime(m[date_key], date_format)
            m['timestamp'] = ts
        yield m


def group_by(items, key):
    groups = defaultdict(list)
    for item in items:
        groups[item[key]].append(item)
    return dict(groups)


def count(items, key):
    counts = defaultdict(int)
    for item in items:
        counts[item[key]] += 1
    return dict(counts)


def bucketize(items):
    # Bucketsize = 1 minute
    bucket = []
    ts = None
    for item in items:
        if item is None:
            continue
        dt = (item['timestamp'].year,
              item['timestamp'].month,
              item['timestamp'].day,
              item['timestamp'].hour,
              item['timestamp'].minute)
        if ts is None:
            ts = dt
            bucket.append(item)
            continue
        if ts != dt:
            ts = dt
            t = bucket[0]['timestamp'].replace(second=0, microsecond=0)
            yield t, bucket
            bucket = []
        bucket.append(item)
    if bucket != []:
        t = bucket[0]['timestamp'].replace(second=0, microsecond=0)
        yield t, bucket


# https://en.wikipedia.org/wiki/Apdex
def apdex(items, target, tolerablefactor=4):
    tolerabletarget = target * tolerablefactor
    total = len(items)
    if total == 0:
        return None, 0
    untolerable = len([f for f in items if f > tolerabletarget])
    satisfied = len([f for f in items if f <= target])
    if untolerable == 0:
        tolerable = 0
    else:
        tolerable = total - untolerable - satisfied
    return (satisfied + (tolerable / 2.0)) / total, total
