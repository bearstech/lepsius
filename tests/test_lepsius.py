import sys
sys.path.append(".")
from lepsius import count


def test_count():
    a = [dict(name="peas", kind="vegetable"),
         dict(name="orange", kind="fruit"),
         dict(name="strawberry", kind="fruit")]
    c = count(a, "kind")
    assert c['fruit'] == 2
    assert c['vegetable'] == 1

test_count()
