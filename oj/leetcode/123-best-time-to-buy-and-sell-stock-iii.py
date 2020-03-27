
"""
- Reduce prices to peaks and troughs:
    highs: [3, 4, 6, 7]
    lows:  [1, 2, 4, 5]
- Iterate all 2-part slicing on highs-lows pair.
for split in range(0, length-of-lows):
    use D&C to calculate max profit of left part
    use max(highs[s:]) - lows[s] to calculate max profit of right part
    profit-of-one-split = profit of left + profit of right
final result is the maximum of all profit-of-one-split
"""

from typing import List

class Solution:
    def __init__(self):
        self.prices = None
        self.highs = []
        self.lows = []
        self.subs = {}  # { "4-7": (5, 2, 9) }, val (max profit, min, max)

    def reduce(self, prices):
        for idx, p in enumerate(prices):
            if idx == 0:
                if p < prices[idx + 1]:
                    self.lows.append(p)
            elif idx == len(prices) - 1:
                if prices[idx - 1] < p:
                    self.highs.append(p)
            else:
                if prices[idx - 1] >= p < prices[idx + 1]:
                    self.lows.append(p)
                elif prices[idx - 1] < p >= prices[idx + 1]:
                    self.highs.append(p)

    def maxWithOneTradeOnHl(self, s: int, e: int):
        if s < 0 or e < 0:
            raise ValueError
        if e - s == 1:
            h, l = self.highs[s], self.lows[s]
            return h - l, l, h
        key = f"{s}-{e}"
        if key in self.subs:
            return self.subs[key]
        half = (e - s) // 2 + s
        l_profit, l_min, l_max = self.maxWithOneTradeOnHl(s, half)
        r_profit, r_min, r_max = self.maxWithOneTradeOnHl(half, e)
        cross_profit = max(r_max - l_min, 0)
        max_profit = max(l_profit, r_profit, cross_profit)
        r = (max_profit, min(l_min, r_min), max(l_max, r_max))
        self.subs[key] = r
        return r

    def maxProfit(self, prices: List[int]) -> int:
        if len(prices) <= 1:
            return 0
        self.reduce(prices)
        assert len(self.lows) == len(self.highs)
        p_len = len(self.lows)
        if p_len < 1:
            return 0
        elif p_len == 1:
            return self.highs[0] - self.lows[0]
        result = 0
        for split in range(len(self.lows)):
            l_profit = self.maxWithOneTradeOnHl(0, split)[0] if split > 0 else 0
            r_profit = max(0, max(self.highs[split:]) - self.lows[split])
            result = max(result, l_profit + r_profit)
        return result
