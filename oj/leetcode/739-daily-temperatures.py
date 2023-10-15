from typing import List

class Solution:
    def dailyTemperatures(self, temperatures: List[int]) -> List[int]:
        mono_stack = []
        result = [0] * len(temperatures)
        for idx, t in enumerate(temperatures):
            if not mono_stack:
                mono_stack.append(idx)
                continue

            while mono_stack and t > temperatures[mono_stack[-1]]:
                result[mono_stack[-1]] = idx - mono_stack[-1]
                mono_stack.pop()
            mono_stack.append(idx)
        return result