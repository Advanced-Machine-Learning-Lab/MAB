from agent import BaseAgent
from agent import BanditProblem


class MMAB(BaseAgent, BanditProblem):
    def __init__(self, neighbour_nodes, agent_num, arm_num, round_num, arms, arms_distribution):
        BaseAgent.__init__(self, neighbour_nodes, agent_num)
        BanditProblem.__init__(self, arms, arm_num, round_num, arms_distribution)

    def pull(self, arm_index):
        return self.reward_distribution(arm_index)
