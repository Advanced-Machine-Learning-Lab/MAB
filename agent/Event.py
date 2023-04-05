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
    事件类
    定义：事件名称：事件队列：
    事件队列存储的是一系列正整数，表示事件多久后发生。
    考虑到每次Agent都需要知道每个事件的「最早发生时间」，因此事件队列仍然使用的是优先队列。
"""


class Event(object):
    def __init__(self):
        self.event_dict = {'decision_making': EventPriorityQueue(),
                           'reward_arriving': EventPriorityQueue(),
                           'message_sending': EventPriorityQueue(),
                           'message_receiving': EventPriorityQueue()}

    """
        获取时间值最小的事件及时间
    """

    def get_nearest_event(self):
        try:
            return min([(e, self.event_dict[e].top()) for e in self.event_dict if self.event_dict[e].qsize() > 0],
                       key=lambda x: x[1])
        except ValueError:
            return None, None

    """
        获取当前标志位为1的事件
    """

    def get_event_value_one_list(self):
        ev_list = []
        for e in self.event_dict:
            if self.event_dict[e].top() == 1:
                ev_list.append((e, self.event_dict[e].get()))

        return ev_list

    """
        将所有大于1的事件的时间减1
    """

    def update_event_time(self):
        for event in self.event_dict:
            self.event_dict[event].minus()

    """
        根据事件名称设定时间
    """

    def set_event_time(self, event, t):
        if event not in self.event_dict or not isinstance(t, int) or t < 0:
            return
        self.event_dict[event].put(t)

    """
        查找事件是否存在
    """

    def is_event_in_list(self, event) -> bool:
        return event in self.event_dict

    """
        获取所有的事件
    """

    def get_all_events(self) -> list:
        return [e for e in self.event_dict]


if __name__ == '__main__':
    ev = Event()
    ev.set_event_time('decision_making', 1)
    ev.set_event_time('decision_making', 3)
    ev.set_event_time('decision_making', 5)

    ev.set_event_time('reward_arriving', 1)
    ev.set_event_time('reward_arriving', 3)
    ev.set_event_time('reward_arriving', 5)

    ev.set_event_time('message_sending', 1)
    ev.set_event_time('message_sending', 3)
    ev.set_event_time('message_sending', 5)

    ev.set_event_time('message_receiving', 1)
    ev.set_event_time('message_receiving', 3)
    ev.set_event_time('message_receiving', 5)
    ret = ev.get_event_value_one_list()
    print(ret)
    for event_name, event_time in ret:
        print(f'event_name:{event_name}, event_time:{event_time}')

    ret = ev.get_event_value_one_list()
    for event_name, event_time in ret:
        print(f'event_name:{event_name}, event_time:{event_time}')

