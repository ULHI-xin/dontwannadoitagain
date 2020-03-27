class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        if len(prices) <= 1:
            return 0
        if len(prices) == 2:
            a, b = prices
            return max(b - a, 0)
        # prices decreasing check, seems not very helpful.
        # if all(prices[i] > prices[i + 1] for i in range(0, len(prices) - 1)):
        #     return 0
        half = len(prices) // 2
        l, r = prices[:half], prices[half:]
        cross_profit = max(max(r) - min(l), 0)
        return max(self.maxProfit(l), self.maxProfit(r), cross_profit)
