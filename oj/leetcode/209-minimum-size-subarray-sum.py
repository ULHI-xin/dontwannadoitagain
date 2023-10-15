from typing import List

class Solution:
    def minSubArrayLen(self, target: int, nums: List[int]) -> int:
        l = 0
        sub_sum = 0
        sub_len = 0
        min_len = 0

        for r in range(len(nums)):
            sub_sum += nums[r]
            sub_len += 1

            if sub_sum < target:
                continue
            
            min_len = sub_len if min_len == 0 else min(min_len, sub_len)
            print(f"(add) min_len={min_len}, l={l}, r={r}, sub_sum={sub_sum}")

            while sub_sum >= target:
                sub_sum -= nums[l]
                sub_len -= 1
                if sub_sum >= target:
                    min_len = sub_len if min_len == 0 else min(min_len, sub_len)
                    print(f"(remove) min_len={min_len}, l={l}, r={r}, sub_sum={sub_sum}")
                l += 1
        return min_len

# target = 7
# nums = [2,3,1,2,4,3]

# target = 4
# nums = [1,4,4]

target = 11
nums = [1,1,1,1,1,1,1,1]

print(Solution().minSubArrayLen(target, nums))