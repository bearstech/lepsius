from collections import defaultdict


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
            yield bucket
            bucket = []
        bucket.append(item)
    if bucket != []:
        yield bucket


# https://en.wikipedia.org/wiki/Apdex
def apdex(items, target, tolerablefactor=4):
    tolerabletarget = target * tolerablefactor
    total = len(items)
    tolerable = total - len(list(filter(lambda f: f > tolerabletarget, items)))
    satisfied = len(list(filter(lambda f: f <= target, items)))
    return (satisfied + tolerable / 2.0) / total
