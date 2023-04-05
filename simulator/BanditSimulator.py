from queue import PriorityQueue

from simulator import Simulator
from agent import MABAgentFactory, AgentQueueElement

"""
    考虑到Simulator每次选择的Agent是「最早发生事件」的Agent
    那么Simulator内部应维护一个按照「最早发生事件」所对应「时间t」来对Agent进行排序的「优先队列」。
    
    另外，考虑到Agent在队列中可能会出现「饥饿」问题，所有进入队列的Agent都会搭上时间戳，Agent出队后再次进队时、时间戳+1。
    
    PriorityAgent将Final Agent封装并进入优先队列（最小堆）
    首先比较的是Agent最近发送事件的时间t，先取出最近发生事件的Agent。
    然后比较的是时间戳timestamp。每个Agent进入队列前都会打上时间戳。在时间t相等的情况下，更早进入队列的Agent会被更优先选择。
"""


class BanditSimulator(Simulator):
    def __init__(self, round_number):
        self.round_number = round_number
        self.agent_num, self.agents, edges, self.neighbour_nodes = MABAgentFactory.get_agent_list(self.round_number)
        # 初始化Router
        for agent in self.agents:
            agent.addresses = self.agents
        self.topology()
        # 初始化Agent队列
        self.queue = PriorityQueue()
        for agent in self.agents:
            print(agent)
            self.queue.put(AgentQueueElement(agent, agent.update(), 1))
        # 初始化边
        self.edges = {}
        for u, v, w in edges:
            if u not in self.edges:
                d = {v: w}
                self.edges[u] = d
            else:
                if v not in self.edges[u]:
                    self.edges[u][v] = w
                else:
                    self.edges[u][v] = min(self.edges[u][v], w)
        self.link_delay()

    """
        topology()
        拓扑函数：给每个节点赋予邻居节点（默认是全连通的）
    """

    def topology(self):
        for i, agent in enumerate(self.agents):
            # agent.addresses = self.agents
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
        while self.queue.qsize():
            agent_node = self.queue.get()
            agent = agent_node.agent
            time_stamp = agent_node.time_stamp
            next_t = agent.update()
            if next_t is None or next_t == 0 or next_t == -1:
                continue
            # 只要当前agent还有下一个时刻，就继续放入优先队列
            self.queue.put(AgentQueueElement(agent, next_t, time_stamp + 1))
        for agent in self.agents:
            print("-----")
            # print(agent.arms_sample_nums)
            print(agent.arms_mean)
            # print("-----")


if __name__ == '__main__':
    banditSi = BanditSimulator(1000)
    banditSi.main()