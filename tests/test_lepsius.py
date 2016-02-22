from datetime import datetime

import sys
sys.path.append(".")
from lepsius import count, bucketize, group_by, apdex


def test_count():
    a = [dict(name="peas", kind="vegetable"),
         dict(name="orange", kind="fruit"),
         dict(name="strawberry", kind="fruit")]
    c = count(a, "kind")
    assert c['fruit'] == 2
    assert c['vegetable'] == 1


def test_bucketize():
    a = [dict(timestamp=datetime(2015, 10, 7, hour=21, minute=33, second=27),
              status='404'),
         dict(timestamp=datetime(2015, 10, 7, hour=21, minute=33, second=42),
              status='404'),
         dict(timestamp=datetime(2015, 10, 7, hour=21, minute=33, second=27),
              status='200'),
         dict(timestamp=datetime(2015, 10, 7, hour=21, minute=42, second=27),
              status='200'),
         ]
    for t, b in bucketize(a):
        g = group_by(b, 'status')
        for status, line in g.items():
            print(status, len(line))


def test_apdex():
    a = range(10)
    ap, total = apdex(a, 2)
    assert 0.6 == ap


test_count()
test_bucketize()
test_apdex()
