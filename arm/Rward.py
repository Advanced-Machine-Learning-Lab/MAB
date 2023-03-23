import numpy as np


class Reward:
    def __init__(self, mean, variance) -> None:
        self.mean = mean
        self.variance = variance

    def reward(self, state, action):
        raise NotImplementedError


class BanditReward(Reward):
    def __init__(self, mean, variance = None) -> None:
        super().__init__(mean, variance)

    def reward(self, state, action):
        return 1 if np.random.rand() <= self.mean else 0