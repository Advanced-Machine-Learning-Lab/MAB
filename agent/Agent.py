import numpy as np


class BaseAgent:

    def __init__(self, arm_number, agent_number) -> None:
        self.arm_number = arm_number
        self.agent_number = agent_number
        self.arm_mean = np.zeros(self.arm_number, dtype=np.float64)
        self.arm_means = np.zeros((self.agent_number, self.arm_number), dtype=np.float64)
        self.arm_rewards = np.zeros((self.agent_number, self.arm_number), dtype=np.float64)
        self.arm_sample_nums = np.zeros((self.agent_number, self.arm_number), dtype=np.float64)
        self.ind_rew = 0
