import socket
from datetime import datetime


class GraphiteClient:

    def __init__(self, host='localhost', port=2003):
        self.host = host
        self.port = port
        self._socket = None

    @property
    def _lazy_socket(self):
        if self._socket is None:
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._socket.connect((self.host, self.port))
        return self._socket

    def send(self, key, value, ts=datetime.now()):
        self._lazy_socket.sendall("%s %d %d\n" % (key, value,
                                                  int(ts.timestamp())))


if __name__ == '__main__':
    gc = GraphiteClient()
    gc.send('pim.pam.poum', 42)
