import heapq
from queue import PriorityQueue


"""
    定义事件队列使用的优先队列
"""


class EventPriorityQueue(PriorityQueue):
    def top(self):
        if len(self.queue) > 0:
            return self.queue[0]
        return None

    def minus(self):
        for i in range(len(self.queue)):
            if self.queue[i] > 1:
                self.queue[i] -= 1
        heapq.heapify(self.queue)


"""
    定义Message队列使用的优先队列
"""


class MessagePriorityQueue(PriorityQueue):
    def top(self):
        if len(self.queue) > 0:
            return self.queue[0]
        return None

    def minus(self):
        for i in range(len(self.queue)):
            self.queue[i].t -= 1
        heapq.heapify(self.queue)