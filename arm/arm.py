class BaseArm:
    def __init__(self, state_space, state_transfor_func, reward_func) -> None:
        self.state_space = state_space
        self.state_transfor_func = state_transfor_func
        self.reward_func = reward_func
        pass

    def __init__(self) -> None:
        pass
    
    def step(self, state, action):
        raise NotImplementedError

    def reset(self):
        raise NotImplementedError

class Reward:
    def __init__(self, mean, variance) -> None:
        self.mean = mean
        self.variance = variance
    
    def reward(self, state, action):
        raise NotImplementedError

import numpy as np

    
class BanditReward(Reward):
    def __init__(self, mean, variance = None) -> None:
        super().__init__(mean, variance)

    def reward(self, state, action):
        return 1 if np.random.rand() <= self.mean else 0

class BanditArm(BaseArm):
    def __init__(self, reward_func) -> None:
        super().__init__()
        self.state_space = {0}
        self.state_transfor_func = lambda x: x # Bandit只有一个state
        self.reward_func = reward_func
        
    def step(self, state = None, action = None):
        return self.state_transfor_func(state), self.reward_func.reward(state, action)

    def reset(self):
        return self
    

class BanditArmFactory:
    @staticmethod
    def get(arm_distribution):
        bandit_reward_func = [BanditReward(x) for x in arm_distribution]
        return [BanditArm(reward_func) for reward_func in bandit_reward_func]