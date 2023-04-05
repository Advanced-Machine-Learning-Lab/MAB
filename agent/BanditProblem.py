import numpy as np
from abc import ABC


from agent import BaseProblem


class BanditProblem(BaseProblem, ABC):
    def __init__(self, arms, arm_num, round_num, arms_distribution):
        self.arms = arms  # 决策集子集
        self.arm_num = arm_num
        self.round_num = round_num
        self.arms_distribution = arms_distribution

        self.arms_means = None  # 对决策集分布的估计
        self.arms_rewards = None  # 累计奖励
        self.arms_sample_nums = None  # 对决策集的采样次数

        # 用于自身估计
        self.arms_mean = None
        self.arms_reward = None
        self.arms_sample_num = None

    def reward_distribution(self, arm_index):
        if np.random.random() <= self.arms_distribution[arm_index]:
            return 1
        return 0

