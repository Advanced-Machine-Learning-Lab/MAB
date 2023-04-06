from abc import ABCMeta, abstractmethod


"""
    Simulator:
    每个agent内部维护时间t、事件-时间队列
    在agent队列中找最快要发生事件的agent:
        next_t = agent.update()
        next_t是该agent下一次发生事件的时间
        将(agent, next_t)放回队列
"""


class Simulator(object, metaclass=ABCMeta):
    @abstractmethod
    def __init__(self):
        raise NotImplementedError

    """
    topology()
    拓扑函数：给每个节点赋予邻居节点（默认是全连通的）
    这部分可以用来初始化每个Final Agent的Router
    """
    @abstractmethod
    def topology(self) -> None:
        raise NotImplementedError

    """
    链路时延函数：获取每个节点到某邻居节点的距离。默认为0。
    """
    @abstractmethod
    def link_delay(self) -> int:
        raise NotImplementedError
