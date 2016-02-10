import socket
from datetime import datetime


class CarbonClient:

    def __init__(self, host='localhost', port=2003):
        self.host = host
        self.port = port
        self._socket = None
        self.prefix = "lepsius.%s" % socket.gethostname()

    @property
    def _lazy_socket(self):
        if self._socket is None:
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._socket.connect((self.host, self.port))
        return self._socket

    def send(self, key, value, ts=datetime.now()):
        assert type(ts) == datetime
        line = u"%s.%s %d %d\n" % (self.prefix, key,
                                   value,
                                   int(ts.timestamp())
                                   )
        self._lazy_socket.sendall(bytes(line, 'utf-8'))


if __name__ == '__main__':
    cc = CarbonClient()
    cc.send('pim.pam.poum', 42)
