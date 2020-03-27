
# Try D&C?

class Solution:
    def __init__(self):
        self.results = []

    def ip(self, s: str, seg: int, prev: List):
        if len(s) > 3 * seg or seg > len(s):
            return
        if seg == 1:
            if int(s) <= 255 and not (len(s) >= 2 and s[0] == '0'):
                self.results.append('.'.join(prev + [s]))
            return
        for i in range(1, 4):
            if i < len(s):
                l, r = s[:i], s[i:]
                if int(l) <= 255 and not (len(l) >= 2 and l[0] == '0'):
                    self.ip(r, seg - 1, prev + [l])

    def restoreIpAddresses(self, s: str) -> List[str]:
        self.ip(s, 4, [])
        return self.results
