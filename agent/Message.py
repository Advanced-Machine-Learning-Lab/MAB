"""
Message类用于通信
"""
import heapq
from collections import deque
from queue import PriorityQueue


class MessagePriorityQueue(PriorityQueue):
    def top(self):
        if len(self.queue) > 0:
            return self.queue[0]
        return None

    def minus(self):
        for i in range(len(self.queue)):
            self.queue[i].t -= 1
        heapq.heapify(self.queue)


class MessageQueueElement(object):
    def __init__(self, message, t):
        self.message = message
        self.t = t

    def __lt__(self, other):
        return self.t < other.t

    def __str__(self):
        return f'mess:{self.message}, t:{self.t}'


class Message(object):
    def __init__(self):
        # 存储其他Agent发送过来的消息
        self.recv_msg_buf = deque()

        # 存储当前Agent发给自己的消息，类似内存缓冲区、用于进程间通信
        self.self_msg_buf = deque()

        # 存储当前Agent发送给其他Agent的消息
        self.send_msg_buf = MessagePriorityQueue()

    """
    组装消息报文
    通信报文格式：{'from_agent_index': int, 'to_agent_index': int, 'arm_index': int, 'reward': float, 'sample_num': float}
    """
    @staticmethod
    def construct_message(from_agent_index, to_agent_index, arm_index, reward, sample_num):
        return {'from_agent_index': from_agent_index, 'to_agent_index': to_agent_index, 'arm_index': arm_index,
                'reward': reward, 'sample_num': sample_num}

    """
        更新send_msg_buf中的时间，将所有大于一的时间减一
    """
    def update_send_buf_time(self):
        self.send_msg_buf.minus()

    """
        将send_msg_buf中积压的消息发送出去
    """

    def _send_message_in_send_msg_buf(self):

        while self.send_msg_buf.top() is not None and self.send_msg_buf.top().t == 1:
            self.send_message(self.send_msg_buf.get().message)

    """
        
    """
    def receive_message(self, other=True) -> list:
        message_list = []
        if other:
            while self.recv_msg_buf:
                message_list.append(self.recv_msg_buf.popleft())
        else:
            while self.self_msg_buf:
                message_list.append(self.self_msg_buf.popleft())
        return message_list

    # other=True表示是由其他Agent发送的消息，否则是自己发送给自己的
    def send_message(self, message, other=True) -> None:
        if other:
            # 从Router中获取邻居节点的内存地址
            to_agent = self.addresses[message['to_agent_index']]
            to_agent.recv_msg_buf.append(message)
        else:
            self.self_msg_buf.append(message)