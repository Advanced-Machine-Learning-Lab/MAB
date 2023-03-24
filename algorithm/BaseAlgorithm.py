from simulator import BaseSimulator


class BaseAlgorithm(BaseSimulator):
    def __init__(self, neighbour_nodes, agent_num, arm_num, round_num, arms, arms_distribution):
        super().__init__(neighbour_nodes, agent_num, arm_num, round_num, arms, arms_distribution)

    def is_communication(self):
        pass

    def arm_selection(self, t):
        pass
