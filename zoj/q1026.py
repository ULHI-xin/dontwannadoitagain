

def poly_product(n0, n1):
    r = set()
    for x in n0:
        for y in n1:
            p = x + y
            if p in r:
                r.remove(p)
            else:
                r.add(p)
    return sorted(r, reverse=True)


def poly_mod(n0, n1):
    if not n0:
        return set(), -1
    r = set(n0)
    h_r = n0[0]
    while h_r >= n1[0]:
        current_q = h_r - n1[0]
        for x in n1:
            p = current_q + x
            if p in r:
                r.remove(p)
            else:
                r.add(p)
        if not r:
            h_r = -1
            break
        h_r = max(r)
    return (r, h_r)


def run(n0, n1, n2):
    def _parse(n):
        n = [int(_n) for _n in n.split(' ')]
        return [n[0] - idx for idx, _n in enumerate(n) if idx > 0 and n[0] - idx >= 0 and _n == 1]
    r, h_r = poly_mod(poly_product(_parse(n0), _parse(n1)), _parse(n2))
    r = [str(h_r + 1)] + ['1' if idx in r else '0' for idx in xrange(h_r, -1, -1)]
    return ' '.join(r)


import sys
t = None
inputs = []
lines = []
for line in sys.stdin:
    line = line.strip()
    if not line or t == 0:
        continue
    if t is None:
        t = int(line)
        continue
    inputs.append(line)
    if len(inputs) == 3:
        print run(inputs[0], inputs[1], inputs[2])
        inputs = []
        t -= 1
        if t == 0:
            continue

