# class Solution:
#     class M:
#         def __init__(self, idx, val):
#             self.idx = idx
#             self.val = val
#
#     def subarraysWithKDistinct(self, A: List[int], K: int) -> int:
#         maxs = 0
#         m_list = []
#         val2m = {}
#         result = 0
#         for idx, v in enumerate(A):
#             # print(f"idx={idx}")
#             if v in val2m:
#                 m_list.remove(val2m[v])
#             val2m[v] = Solution.M(idx, v)
#             m_list.append(val2m[v])
#             if len(val2m) == K:
#                 result += m_list[0].idx - maxs + 1
#                 # print(f"result={result}")
#             elif len(val2m) > K:
#                 to_remove = m_list[0]
#                 m_list.remove(to_remove)
#                 val2m.pop(to_remove.val)
#                 for i in range(to_remove.idx + 1, idx + 1):
#                     if A[i] != to_remove.val:
#                         maxs = i
#                         break
#                 result += m_list[0].idx - maxs + 1
#                 # print(f"result={result}")
#             # print([m.val for m in m_list])
#             # print([m.idx for m in m_list])
#             # print({val: m.idx for val, m in val2m.items()})
#         return result

# User OrderedDict, but no drastic improving.
from typing import List
from collections import OrderedDict
class Solution:
    class MOD(OrderedDict):
        def item0(self):
            for k, v in self.items():
                return k, v
            return None, None
    def subarraysWithKDistinct(self, A: List[int], K: int) -> int:
        maxs = 0
        val2m = Solution.MOD()
        result = 0
        for idx, v in enumerate(A):
            # print(f"idx={idx}")
            if v in val2m:
                val2m.pop(v)
            val2m[v] = dict(i=idx, v=v)
            if len(val2m) == K:
                _, v0 = val2m.item0()
                result += v0['i'] - maxs + 1
                # print(f"result={result}")
            elif len(val2m) > K:
                k_to_remove, v_to_remove = val2m.item0()
                val2m.pop(k_to_remove)
                for i in range(v_to_remove['i'] + 1, idx + 1):
                    if A[i] != v_to_remove['v']:
                        maxs = i
                        break
                _, v0 = val2m.item0()
                result += v0['i'] - maxs + 1
                # print(f"result={result}")
            # print({val: m['i'] for val, m in val2m.items()})
        return result
