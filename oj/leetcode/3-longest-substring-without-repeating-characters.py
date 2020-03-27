# Try D&C, should be faster.

class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        non_rightmost_len = 0
        rightmost = ''
        rightmost_len = 0
        for c in s:
            if c not in rightmost:
                rightmost += c
                rightmost_len += 1
            else:
                if rightmost_len > non_rightmost_len:
                    non_rightmost_len = rightmost_len
                rightmost += c
                rightmost = rightmost[rightmost.find(c) + 1:]
                rightmost_len = len(rightmost)
        return max(rightmost_len, non_rightmost_len)
