import numpy as np

from .Policy import BasePolicy
from agent.DOEAgent import DOEAgent


class DOEPolicy(BasePolicy):
    def __init__(self, agent, arm_number) -> None:
        super().__init__(agent, arm_number)
        self.candidate_set = np.ones(self.arm_number)
        self.index = 0

    def select_arm(self):
        while self.index < self.arm_number and self.candidate_set[self.index] == 0:
            self.index = (self.index + 1) % self.arm_number
        cur_index = self.index
        self.index = (self.index + 1) % self.arm_number
        return cur_index

    def is_communicated(self, args):
        arm_i, common_mean, ei = args['arm_i'], args['common_mean'], args['ei']
        return np.abs(self.agent.arm_mean[arm_i] - common_mean) > ei and ei < 1
