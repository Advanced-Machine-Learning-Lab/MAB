"""
Simulator的作用是整合静态的资源，比如 agent、arm和policy
Simulator内部进行运算，返回时序信息
"""
from communication import Communication


class BaseSimulator(object):
    # 传入agent、arms和policy均为实例的引用
    def __init__(self, agents: list, arms: list, policies: list, communication: Communication, T: int) -> None:
        self.agents = agents
        self.arms = arms
        self.policies = policies
        self.agent_number = len(self.agents)
        self.arms_number = len(self.arms)
        self.communication = communication
        self.communication_times = 0
        self.T = T
        self.t = 0
        self.regret = 0

    def __iter__(self):
        raise NotImplementedError

    def __next__(self):
        raise NotImplementedError
