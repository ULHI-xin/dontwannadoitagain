ctt, wtt = False, False
def can_do(c, w, idx):
    for i in xrange(idx, 101):
        if c % i == 0:
            if can_do(c / i, w, i + 1):
                return True
        if w % i == 0:
            if can_do(c, w / i, i + 1):
                return True
    global ctt
    global wtt
    if c == 1 and w == 1:
        return True
    if c == 1:
        ctt = True
        return False
    if w == 1:
        wtt = True
        return False
    return False

# import sys
# for line in sys.stdin:
#     a = line.split()
#     ctt = False
#     wtt = False
#     num0, num1 = int(a[0]), int(a[1])
#     if num0 == num1:
#         print(num0)
#     else:
#         _chlg, _winner = (num0, num1) if num0 < num1 else (num1, num0)
#         if _winner <= 100:
#             print _winner
#             continue
#         if can_do(_chlg, _winner, 2):
#             print _winner
#         else:
#             if not ctt:
#                 print _winner
#             else:
#                 print _chlg

while True:
    line = raw_input()
    if not line.strip():
        break
    c_tell_truth = False
    num0, num1 = [long(x) for x in line.split(' ')]
    if num0 == num1:
        print(num0)
    else:
        _chlg, _winner = (num0, num1) if num0 < num1 else (num1, num0)
        if _winner <= 100:
            print(_winner)
            continue
        if can_do(_chlg, _winner, 1):
            print(_winner)
        else:
            print(_chlg)
