from io import StringIO
from datetime import datetime

import sys
sys.path.append(".")

from lepsius import influxdb


def test_escape():
    assert r"pim\,\ pam\,\ poum" == influxdb.escape("pim, pam, poum")


def test_serialize():
    out = StringIO()
    influxdb.serialize(out, "cpu", dict(load=10.0, alert=True),
                       dict(host="Server A", region="us west"),
                       datetime(2015, 2, 22, 17, 55))
    out.seek(0)
    r = out.readlines()
    assert "cpu,host=Server\ A,region=us\ west alert=t,load=10.0 1424624100000000000\n" == r[0]
