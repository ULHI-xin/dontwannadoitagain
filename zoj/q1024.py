def add_month(y, m, d):
    r = None
    if d <= 28:
        r = (y, m + 1, d)
    elif d == 30:
        if m == 1:
            r = None
        else:
            r = (y, m + 1, 30)
    elif d == 31:
        if m == 12 or m == 7:
            r = (y, m + 1, 31)
        else:
            r = None
    elif d == 29:
        if m == 1 and (y % 4 != 0 or y == 1900):
            r = None
        else:
            r = (y, m + 1, 29)
    if not r:
        return None
    if r[1] == 13:
        return r[0] + 1, 1, r[2]
    return r


def days_of_month(y, m):
    if m == 2:
        if y % 4 == 0 and y != 1900:
            return 29
        return 28
    if m in {4, 6, 9, 11}:
        return 30
    return 31


def add_day(y, m, d):
    if d + 1 > days_of_month(y, m):
        r = (y, m + 1, 1)
    else:
        r = (y, m, d + 1)
    if r[1] == 13:
        return r[0] + 1, 1, r[2]
    return r


def minus_day(y, m, d):
    if d >= 2:
        return y, m, d - 1
    if m == 1:
        return y - 1, 12, 31
    return y, m - 1, days_of_month(y, m - 1)


def gen_for_20011104():
    r = {20011104, }
    y, m, d = 2001, 11, 04
    while True:
        y, m, d = minus_day(y, m, d)
        int_c = y * 10000 + m * 100 + d
        if int_c <= 19000101:
            break
        day_after = add_day(y, m, d)
        if day_after:
            day_after_yes = (day_after[0] * 10000 + day_after[1] * 100 + day_after[2]) in r
        else:
            day_after_yes = False
        month_after = add_month(y, m, d)
        if day_after_yes:
            continue
        if month_after:
            month_after_yes = (month_after[0] * 10000 + month_after[1] * 100 + month_after[2]) in r
        else:
            month_after_yes = False
        if month_after_yes:
            continue
        r.add(int_c)
    return r


import sys
t = None
all_yes = gen_for_20011104()
for line in sys.stdin:
    line = line.strip()
    if not line:
        break
    if t is None:
        t = int(line)
        continue
    y, m, d = [int(x) for x in line.split(' ')]
    c_int = y * 10000 + m * 100 + d
    if c_int in all_yes:
        print 'NO'
    else:
        print 'YES'

