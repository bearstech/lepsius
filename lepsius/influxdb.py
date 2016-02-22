import socket
from datetime import datetime


def escape(txt):
    return txt.translate(str.maketrans({",": "\,",
                                        " ": "\ "}))


def escape_quote(txt):
    return txt.translate(str.maketrans({",": r"\,",
                                        " ": r"\ ",
                                        '"': r'\"'}))


def serialize(output, key, fields, flags=None, ts=None):
    output.write(escape(key))
    if flags is not None:
        for k in sorted(flags.keys()):
            output.write(',')
            output.write(escape(k))
            output.write('=')
            output.write(escape(str(flags[k])))
    output.write(" ")
    prems = True
    for k in sorted(fields.keys()):
        if prems:
            prems = False
        else:
            output.write(",")
        output.write(k)
        output.write("=")
        v = fields[k]
        t = type(v)
        if t == int:
            output.write(str(v))
            output.write('i')
        elif t == bool:
            output.write('t' if t else 'f')
        elif t == float:
            output.write(str(v))
        else:  # it should a string
            output.write('"')
            output.write(escape_quote(str(v)))
            output.write('"')
    if ts is not None:
        output.write(' ')
        output.write(str(int(ts.timestamp() * 1000000000)))
    output.write("\n")


class InfluxdbClient:

    def __init__(self, db='lepsius', host='localhost', port=8086):
        self.host = host
        self.port = port

    def send(self, key, values, flags=None, ts=None):
        pass
