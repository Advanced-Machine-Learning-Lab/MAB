from agent.utils import AgentQueueElement
from example.singleagent.SingleAgentFactory import SingleAgentFactory
from example.mab.MABAgentFactory import MABAgentFactory

"""
    Simulator:
    每个agent内部维护时间t、事件-时间队列
    在agent队列中找最快要发生事件的agent:
        next_t = agent.update()
        next_t是该agent下一次发生事件的时间
        将(agent, next_t)放回队列

    考虑到Simulator每次选择的Agent是「最早发生事件」的Agent
    那么Simulator内部应维护一个按照「最早发生事件」所对应「时间t」来对Agent进行排序的「队列」。

    另外，考虑到Agent在队列中可能会出现「饥饿」问题，所有进入队列的Agent都会搭上时间戳，Agent出队后再次进队时、时间戳+1。

    PriorityAgent将Final Agent封装并进入队列 
    首先比较的是Agent最近发送事件的时间t，先取出最近发生事件的Agent。
    然后比较的是时间戳timestamp。每个Agent进入队列前都会打上时间戳。在时间t相等的情况下，更早进入队列的Agent会被更优先选择。
    
    注意：当取出一个agent后，该agent可能会改变队列中其他agent的时间（agent发送了消息给邻居agent），所以这个队列不是静态的
            目前的实现没有用最小堆、而是数组
            
            
    使用方法：1、定义好Factory类、写好Factory中get_agent_list()静态方法
            2、实例化一个MultiAgentSimulator，传入Factory和data文件夹地址
            3、运行MultiAgentSimulator中的main()
"""


class MultiAgentSimulator(object):

    def __init__(self, round_number, agent_factory, prefix_path):
        self.round_number = round_number
        self.agent_num, self.agents, self.edges, self.neighbour_nodes = agent_factory.get_agent_list(round_num=self.round_number, prefix_path=prefix_path)
        # 初始化Router
        for agent in self.agents:
            agent.addresses = self.agents
        self.topology()
        # 初始化Agent队列
        self.queue = []
        for agent in self.agents:
            print(agent)
            self.queue.append(AgentQueueElement(agent, t=agent.get_state(), time_stamp=1))
        # 初始化边
        self.link_delay()

    """
        topology()
        拓扑函数：给每个节点赋予邻居节点（默认是全连通的）
    """

    def topology(self):
        for i, agent in enumerate(self.agents):
            agent.neighbour_nodes = self.neighbour_nodes[i]

    """
        链路时延函数：每个节点到某邻居节点的距离。默认为0。
    """

    def link_delay(self) -> None:
        for agent in self.agents:
            agent.edges = self.edges


    """
        Simulator主流程
    """

    def main(self):
        while True:
            # 更新每个agent的状态
            min_t_agent = None
            for cur_agent in self.queue:
                cur_agent.t = cur_agent.agent.get_state()
                if cur_agent.t < 0x3f3f3f3f \
                        and (min_t_agent is None or min_t_agent.t > cur_agent.t):
                    min_t_agent = cur_agent
                elif min_t_agent is not None \
                        and cur_agent.t == min_t_agent.t \
                        and cur_agent.time_stamp < min_t_agent.time_stamp:
                    min_t_agent = cur_agent

            if min_t_agent is None:
                break
            min_t_agent.t = min_t_agent.agent.update()
            min_t_agent.time_stamp += 1


if __name__ == '__main__':
    # 运行MAB例子
    mab_si = MultiAgentSimulator(round_number=10, agent_factory=MABAgentFactory, prefix_path='../example/mab/data')
    mab_si.main()

    # 运行SingleAgent例子
    single_si = MultiAgentSimulator(round_number=10, agent_factory=SingleAgentFactory, prefix_path='../example/singleagent/data')
    single_si.main()