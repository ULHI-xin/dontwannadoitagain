# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    # 1->2->3->4
    # 4->3->2->1
    def foo(self, h, k):
        # h
        # 0 -> 1 -> 2
        # l    c    r
        # 0 <- 1    2
        # l    c    r
        #      l    c​
        test_h = h
        if not h:
            return None, None
        for _ in range(k - 1):
            test_h = test_h.next
            if not test_h:
                return None, None
        c = h.next
        # print(c)
        l = h
        # print(l)
        for _ in range(k - 1):
            r = c.next
            # print(r)
            c.next = l
            # print(l)
        
            l = c
            c = r
        h.next = r
        return l, h

    def reverseKGroup(self, head: Optional[ListNode], k: int) -> Optional[ListNode]:
        if k == 1:
            return head

        first_new_head, tail = self.foo(head, k)
        if not first_new_head:
            return head

        new_head = first_new_head
        # print(f"init new_h={new_head}")
        while new_head:
            # print(f"tail={tail}")
            new_head, new_tail = self.foo(tail.next, k)
            # print(f"new_h={new_head}")
            if new_head:
                tail.next = new_head
            tail = new_tail
        return first_new_head