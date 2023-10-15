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

class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        substr_idx = {}
        max_sub_len = 0
        substr_l = 0
        for idx, c in enumerate(s):
            if c not in substr_idx:
                substr_idx[c] = idx
                max_sub_len = max(max_sub_len, len(substr_idx))
                continue
            idx_to_trunc = substr_idx[c]
            for l in range(substr_l, idx_to_trunc + 1):
                substr_idx.pop(s[l])
            substr_l = idx_to_trunc + 1
            substr_idx[c] = idx
            max_sub_len = max(max_sub_len, len(substr_idx))
        return max_sub_len


s = "abcabcbb"
s = "bbbbb"
s = "pwwkew"
print(Solution().lengthOfLongestSubstring(s))
