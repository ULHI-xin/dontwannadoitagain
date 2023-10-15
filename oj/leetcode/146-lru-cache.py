
class N:
    def __init__(self, k, v) -> None:
        self.k = k
        self.v = v
        self.prev = None
        self.next = None
    
    def __repr__(self) -> str:
        return f"({self.k}={self.v}, P:{self.prev and self.prev.k} N:{self.next and self.next.k})"

class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.lru = {}
        self.L = N(-1, -1)
        self.M = N(-9999999, -1)
        self.L.next = self.M
        self.M.prev = self.L

    def get(self, key: int) -> int:
        if key not in self.lru:
            return -1
        c = self.lru[key]

        p = c.prev
        n = c.next
        p.next = n
        n.prev = p

        self.M.prev.next = c
        c.prev = self.M.prev
        c.next = self.M
        self.M.prev = c

        # print(f"get c={c}")
        # print(f"get M={self.M}")
        # print(f"get L={self.L}")
        # print(f"get {len(self.lru)} cap:{self.capacity} \n")

        return c.v


    def put(self, key: int, value: int) -> None:
        if key in self.lru:
            c = self.lru[key]
            c.v = value
            p = c.prev
            n = c.next
            p.next = n
            n.prev = p
        else:
            c = N(key, value)
        self.M.prev.next = c
        c.prev = self.M.prev
        c.next = self.M
        self.M.prev = c
        self.lru[key] = c

        # print(f"put c={c}")
        # print(f"put M={self.M}")
        # print(f"put L={self.L}")
        # print(f"put {len(self.lru)} cap:{self.capacity} \n")

        if len(self.lru) > self.capacity:
            f = self.L.next
            n = f.next
            self.L.next = n
            n.prev = self.L
            self.lru.pop(f.k)

lRUCache = LRUCache(2)
lRUCache.put(1, 1) # 缓存是 {1=1}
lRUCache.put(2, 2) # 缓存是 {1=1, 2=2}
print(lRUCache.get(1))    # 返回 1
lRUCache.put(3, 3) # 该操作会使得关键字 2 作废，缓存是 {1=1, 3=3}
print(lRUCache.get(2))    # 返回 -1 (未找到)
lRUCache.put(4, 4) # 该操作会使得关键字 1 作废，缓存是 {4=4, 3=3}
print(lRUCache.get(1))    # 返回 -1 (未找到)
print(lRUCache.get(3))    # 返回 3
print(lRUCache.get(4))    # 返回 4


# ["LRUCache","put","put","get","put","put","get"]
# [[2],[2,1],[2,2],[2],[1,1],[4,1],[2]]
# expect: [null,null,null,2,null,null,-1]
# obj = LRUCache(2)
# obj.put(2, 1)
# obj.put(2, 2)