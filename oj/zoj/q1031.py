
def all_square(n):
    def _square_n(_lt, _n, ctx_n, _limit):
        if _lt + _n - 1 >
        _r = []
        dist = 2 * ctx_n + 1
        for x in range(_n):
            _r.append(_lt + x)
            _r.append(_lt + ctx_n + x * dist)
            _r.append(_lt + dist * _n + x)
            _r.append(_lt + ctx_n + _n + dist * x)
        for i in _r:
            if i > _limit:
                return None
        return _r


    r = []
    loopidx = sum([range(1 + (2 * n + 1) * i, 1 + (2 * n + 1) * i + n) for i in range(n)], [])
    limit = n * (n + 1) * 2
    for i in range(1, n + 1):
        for _lt in loopidx:
            sq = _square_n(_lt, i, n, limit)
            if sq:
                r.append(sq)
    return r
