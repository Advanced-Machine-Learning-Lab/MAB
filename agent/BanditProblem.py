import numpy as np
from agent import BaseProblem


class BanditProblem(BaseProblem):
    def __init__(self, arms, arm_num, round_num, arms_distribution):
        super().__init__(arm_num, round_num)
        self.arms = arms
        self.arms_distribution = arms_distribution

    def reward_distribution(self, arm_index):
        if np.random.random() <= self.arms_distribution[arm_index]:
            return 1
        return 0
