import numpy as np

# from agent import MABAgent


# 虚拟类的定义
"""
定义函数
拓扑函数：给每个节点赋予邻居节点（默认是全连通的）
链路时延函数：默认为0


定义事件类（放在BaseAgent里）
触发、动态

Event class

标志变量
algorithm置 其中的值
decision_making = 5
reward_arriving = 0
message_sending = 10
message_receiving = 5

类
Message:
    

[0, 1, 0, 3]
{"decision_making": 0, "reward_arriving":1, "message_sending": 0, "message_receiving":3}

Router:
    存储每个节点的内存地址

Simulator:
    每个agent内部维护一个时间t。
    找最快要发生事件的agent。
    for each agent:
        next_t = agent.update()
        next_t -> 
        

XXXAgent 继承自 BaseAgent + Problem + Algorithm + Message + Router:
    Algorithm-> update():
        看哪个事件是1，就去更新对应的变量。


"""
from abc import ABCMeta, abstractmethod


class Simulator(object):
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
