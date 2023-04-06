from abc import ABC

import numpy as np
from algorithm import BaseAlgorithm
from agent import Message, MessageQueueElement

"""
Algorithm要完成大部分的工作，目前的设计是只开放update()函数。
Simulator从agent队列中寻找最快要发生事件的agent，调用该agent的algorithm中的update()函数。
Algorithm会根据当前agent中的Evnet类中显示此时应该要去做的事件、完成相应的动作，包括：
    1、decision_making（为当前agent选择一个arm、pull一次、发送奖励给自己/邻居）
    2、reward_arriving（接受自己/邻居的奖励）
    3、message_sending（将agent自己的所有信息发送给邻居agent）
    4、message_receiving（接受邻居发送过来的信息，如果该信息中的arm不在自己的决策子集中、丢弃该消息）
注意，这里的设计思路是，只有事件对应的时间t==1时，这件事才会在当前去处理。

BanditAlgorithm只是完成一个「示例」，仅供参考。
Algorithm具有高度的自由，以上4种事件的「具体实现」完全取决于作者的算法设计。
"""


class BanditAlgorithm(BaseAlgorithm, ABC):
    def __init__(self):
        pass

    def set_arm_estimation(self, arms_means, arms_rewards, arms_sample_nums, arms_mean, arms_reward, arms_sample_num):
        self.arms_means = arms_means  # 对决策集分布的估计
        self.arms_rewards = arms_rewards  # 累计奖励
        self.arms_sample_nums = arms_sample_nums  # 对决策集的采样次数
        self.arms_mean = arms_mean
        self.arms_reward = arms_reward
        self.arms_sample_num = arms_sample_num

    """
        update()函数是Algorithm对外开放的函数。
        Simulator调用agent内部algorithm的update()
        update()完成的工作：
                        1、获取每个事件的时间队列。
                        2、若某个事件对应的最先发生时间为1，则执行这一事件。
                        3、更新事件队列中的时间（集体减去一）
                        4、根据Algorithm的需求，增加新的事件进入到队列、指定t秒后发生。
                        5、获取各事件时间队列中的最小值，返回给simulator
        Simulator根据各agent返回的时间t、对agent进行排序。继续选择时间t最小的Agent进行update()。
    """

    def update(self):
        # 算法初始化阶段
        if self.init:
            for _ in self.arms:
                self._decision_making()
                self._reward_arriving()

            self.set_event_time('decision_making', 1)
            self.init = False
            return 1


        # 检查当前时间
        if self.t > self.round_num:
            return -1

        # 找到所有当前标志位为1的事件，分别去执行
        # 全部执行完成后，所有标志位为1的事件、均弹出队列。

        while True:
            # 检查send_msg_buf中是否有当下要发生的消息，若有，则发送消息。
            self._send_message_in_send_msg_buf()
            # 获取事件队列中t=1的事件
            appending_events = self.get_event_value_one_list()
            if appending_events is None or len(appending_events) == 0:
                break
            # 根据事件类型进行执行
            for event_name, event_time in appending_events:
                if event_name == 'decision_making':
                    self._decision_making()
                elif event_name == 'reward_arriving':
                    self._reward_arriving()
                elif event_name == 'message_sending':
                    self._message_sending()
                elif event_name == 'message_receiving':
                    self._message_receiving()

        # 更新send_msg_buf中的时间(集体减去1)
        self.update_send_buf_time()

        # 更新事件队列中的时间(集体减去1)
        self.update_event_time()

        # Agent的时间t+1
        self.t += 1
        # 这里设计的算法是：当前Agent每个时间t都会进行决策
        # 所以下一秒agent会继续做决策
        self.set_event_time('decision_making', 1)
        # 通信策略：设定为self.t == 2^n时发送一次消息
        if int(np.power(2, int(np.log2(self.t)))) == self.t:
            self.set_event_time('message_sending', 1)
        # 找到当前最近要发生的事件的时间
        _, near_t = self.get_nearest_event()
        # 注意：假如事件-时间均为0，那么这里的near_t是None
        return near_t

    """
        _update_agent_on_arm()用于更新Agent获得奖励后对mean等进行更新。
    """
    def _update_agent_on_arm(self):
        if self.init:
            return
        for arm_index in self.arms:
            rewards = 0
            sample_nums = 0.0
            for agent_index in range(self.agent_num):
                rewards += self.arms_rewards[agent_index][arm_index]
                sample_nums += self.arms_sample_nums[agent_index][arm_index]
            self.arms_reward[arm_index] = rewards
            self.arms_sample_num[arm_index] = sample_nums
            self.arms_mean[arm_index] = rewards / sample_nums

    """
        _decision_making()用于Agent做决策：pull arm、发送奖励给自己/其他Agent
    """
    def _decision_making(self):
        # 选择一个arm
        arm_index = self._arm_selection()
        # pull一个arm
        reward = self.pull(arm_index)
        # 向自己发送消息
        # 在一些Bandit问题的设定下，当前Agent对arm_index获得的奖励，其他Agent也可以观测到
        # 此时可以向其他Agent发送消息
        message = Message.construct_message(self.agent_index, self.agent_index, arm_index, reward, 1)
        self.send_message(message, False)
        # 设定1s后奖励到达
        self.set_event_time('reward_arriving', 1)
        if not self.init:
            print(f't:{self.t}, agent:{self.agent_index} pull arm:{arm_index}')

    """
        _reward_arriving()用于Agent接受自己/其他Agent的奖励。
    """
    def _reward_arriving(self):
        # 获取自发送的消息 或者观测到的消息
        message_list = self.receive_message(other=False)
        for message in message_list:
            # 解析消息
            arm_index, reward, sample_num = message['arm_index'], message['reward'], message['sample_num']
            # 更新奖励、次数和估计
            self.arms_rewards[self.agent_index][arm_index] += reward
            self.arms_sample_nums[self.agent_index][arm_index] += sample_num
            self.arms_means[self.agent_index][arm_index] = self.arms_rewards[self.agent_index][arm_index] / \
                                                           self.arms_sample_nums[self.agent_index][
                                                               arm_index]

            if not self.init:
                print(f't:{self.t}, agent:{self.agent_index} get reward:{reward} from arm:{arm_index},')
        self._update_agent_on_arm()

    """
        _message_sending()向邻居节点发送信息
    """
    def _message_sending(self):
        # 遍历当前Agent的决策集
        for arm_index in self.arms:
            # 遍历当前Agent的所有邻居
            for neighbour_node in self.neighbour_nodes:
                # 组装消息报文
                message = Message.construct_message(self.agent_index,
                                                    neighbour_node,
                                                    arm_index,
                                                    self.arms_rewards[self.agent_index][arm_index],
                                                    self.arms_sample_nums[self.agent_index][arm_index])

                # 消息加入等待队列中
                link_delay = self.edges[self.agent_index][neighbour_node] + 1
                mqe = MessageQueueElement(message, link_delay)
                self.send_msg_buf.put(mqe)
                # 告知对方agent取消息的时间
                to_agent = self.addresses[neighbour_node]
                to_agent.set_event_time('message_receiving', link_delay)
                print(
                    f't:{self.t}, agent:{self.agent_index} send message to agent:{neighbour_node}, link_delay:{link_delay}')

    """
        _message_receiving()接受来自邻居节点的信息
    """
    def _message_receiving(self):
        message_list = self.receive_message(other=True)
        for message in message_list:
            # 解析消息
            arm_index, reward, sample_num = message['arm_index'], message['reward'], message['sample_num']
            # 若消息中的arm不在当前Agent决策子集中则丢弃该消息
            if arm_index not in self.arms:
                continue
            from_agent_index = message['from_agent_index']
            self.arms_rewards[from_agent_index][arm_index] = reward
            self.arms_sample_nums[from_agent_index][arm_index] = sample_num
            print(
                f't:{self.t}, agent:{self.agent_index} received message from agent:{from_agent_index} on arm:{arm_index}')
        self._update_agent_on_arm()
        # self.set_event_value('message_receiving', 0)

    """
        _arm_selection()由算法决定选择Arm的策略
    """
    def _arm_selection(self) -> int:
        # 这里以UCB为例子
        # 初始化过程，返回没有pull过的arm
        if self.init:
            for arm_index in self.arms:
                if self.arms_sample_nums[self.agent_index][arm_index] == 0:
                    return arm_index
            return -1
        # 计算当前Agent对每个arm pull的次数
        s_n = np.array([self.arms_sample_nums[self.agent_index][arm_index] for arm_index in self.arms],
                       dtype=np.float64)
        # 计算置信区间
        confidence_interval = np.sqrt(2 * np.log(self.t) / s_n)
        # print(f'self.t{self.t}, confidence_interval:{confidence_interval}')
        # 计算当前Agent对每个arm的mean
        mean = np.array([self.arms_means[self.agent_index][arm_index] for arm_index in self.arms], dtype=np.float64)
        # 取出在决策集子集中、mean+ci最大的值对应的下标
        arm_index_in_sub_arms = np.argmax(mean + confidence_interval)
        # 返回arm的真实下标
        return self.arms[arm_index_in_sub_arms]