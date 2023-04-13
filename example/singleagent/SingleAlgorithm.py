from abc import ABC

from agent import Message
from algorithm import BaseAlgorithm
from agent.utils import MessageQueueElement


class SingleAlgorithm(BaseAlgorithm):
    def __init__(self):
        pass

    """
            get_state() 获取agent的最快发生事件对应的时间
        """

    def get_state(self):
        if self.t > self.round_num:
            return 0x3f3f3f3f
        _, near_t = self.get_nearest_event()
        if self.send_msg_buf.top() is not None:
            return min(self.send_msg_buf.top().t, near_t)
        return near_t

    def update(self):
        if self.t > self.round_num:
            return 0x3f3f3f3f
        while True:
            self._send_message_in_send_msg_buf()
            appending_events = self.get_event_value_one_list()
            if appending_events is None or len(appending_events) == 0:
                break
            # 根据事件类型进行执行
            for event_name, event_time in appending_events:
                if event_name == 'message_sending':
                    self._message_sending()
                elif event_name == 'message_receiving':
                    self._message_receiving()
        # 更新send_msg_buf中的时间
        self.update_send_buf_time()
        # 更新事件队列中的时间
        self.update_event_time()
        self.t += 1
        return self.get_state()

    def _message_sending(self):
        for to_agent_index in self.neighbour_node:
            message = Message.construct_message(self.agent_index,
                                                to_agent_index,
                                                0,
                                                1 + self.num,
                                                1 + self.num)
            # 消息加入等待队列中
            # print(f'self.edges:{self.edges}, agent_index:{self.agent_index}, to_agent_index:{to_agent_index}')
            link_delay = self.edges[self.agent_index][to_agent_index] + 1
            mqe = MessageQueueElement(message, link_delay)
            self.send_msg_buf.put(mqe)
            # 告知对方agent获取消息的时间
            print(f'agent:{self.agent_index}, t:{self.t}, send a message to agent:{to_agent_index}, num:{1 + self.num}')
            to_agent = self.addresses[to_agent_index]
            to_agent.set_event_time('message_receiving', link_delay)

    def _message_receiving(self):
        message_list = self.receive_message(other=True)
        for message in message_list:
            # 解析消息
            sample_num = message['sample_num']
            from_agent_index = message['from_agent_index']
            self.num = sample_num
            print(
                f'agent:{self.agent_index}, t:{self.t}, received a message from agent:{from_agent_index}, num:{sample_num}')
            self.set_event_time('message_sending', 1)
