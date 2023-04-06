import numpy as np
from queue import PriorityQueue

from agent import BaseAgent, BanditProblem, Message, Router, Event
from algorithm import BanditAlgorithm


class MABAgent(BaseAgent, BanditProblem, BanditAlgorithm, Event, Message, Router):
    def __init__(self, agent_num, agent_index, arms, arm_num, arms_distribution, round_num):
        # 调用各父类的构造函数
        BaseAgent.__init__(self, agent_num)
        BanditProblem.__init__(self, arms, arm_num, round_num, arms_distribution)
        BanditAlgorithm.__init__(self)
        Event.__init__(self)
        Message.__init__(self)
        Router.__init__(self)

        # 当前Agent的序号
        self.agent_index = agent_index

        # 初始化当前Agent对arm的采样信息，包括其他Agent发送的信息
        arms_means = np.zeros((self.agent_num, self.arm_num))
        arms_rewards = np.zeros((self.agent_num, self.arm_num))
        arms_sample_nums = np.zeros((self.agent_num, self.arm_num))

        # 初始化当前Agent对arm的mean、reward和采样次数
        arms_mean = np.zeros(self.arm_num)
        arms_reward = np.zeros(self.arm_num)
        arms_sample_num = np.zeros(self.arm_num)
        self.set_arm_estimation(arms_means, arms_rewards, arms_sample_nums, arms_mean, arms_reward, arms_sample_num)

        # 初始化Agent的时间
        self.t = 1

        # 初始化当前Agent的Algorithm
        self.init = True
        # self.algorithm_init()
        self.edges = None

        # Router的初始化应该由外部完成
        # 因为Router存储的是每个Final Agent的内存地址
        # 当前Agent初始化时无法得知其他Agent的内存地址

    """
        返回当前Agent的描述信息
    """

    def __str__(self):
        return f"agent_index:{self.agent_index}, neighbour_nodes:{self.neighbour_nodes}, " \
               f"agent_num:{self.agent_num}, arms:{self.arms}, arm_num:{self.arm_num}, " \
               f"arms_distribution:{self.arms_distribution}, round_num:{self.round_num}"

    """
        当前Agent pull arm_index对应的Arm
    """

    # MABAgent
    def pull(self, arm_index):
        return self.reward_distribution(arm_index)


"""
用于优先队列的数据结构
agent：Final Agent
t：该Agent最近要发生的事件的时刻
time_stamp：该Agent进入队列的时间
Simulator每次从队列中取出t最小的Agent
"""


class AgentQueueElement(object):
    def __init__(self, agent, t, time_stamp):
        self.agent = agent
        self.t = t
        self.time_stamp = time_stamp

    def __lt__(self, other):
        if self.t == other.t:
            return self.time_stamp < other.time_stamp
        return self.t < other.t


if __name__ == '__main__':

    """
    Final Agent允许独立运行
    下面是运行示例
    """

    # update()函数返回值是最近发生事件的时间t，告诉Simulator应该先调度哪个Agent。
    # Simulator内部维护一个优先队列（最小堆）
    mab_agent = MABAgent(agent_num=1, agent_index=0, round_num=10, arm_num=3, arms=[0, 1, 2],
                         arms_distribution=[0.1, 0.4, 0.9])
    mab_agent.addresses = [mab_agent]
    mab_agent.neighbour_nodes = []

    pq = PriorityQueue()
    pq.put(AgentQueueElement(mab_agent, mab_agent.update(), 1))
    print(mab_agent.arms_sample_nums)

    while pq.qsize():
        agent_t = pq.get()
        agent = agent_t.agent
        next_t = agent.update()
        if next_t is None or next_t == 0 or next_t == -1:
            continue
        # 只要当前agent还有下一个时刻，就继续放入优先队列
        pq.put(AgentQueueElement(agent, next_t, 1))

    print(mab_agent.arms_sample_nums)
