class BaseArm:
    def __init__(self, state_space, state_transfor_func, reward_func) -> None:
        self.state_space = state_space
        self.state_transfor_func = state_transfor_func
        self.reward_func = reward_func

    def __init__(self) -> None:
        pass

    def step(self, state, action):
        raise NotImplementedError

    def reset(self):
        raise NotImplementedError


class BanditArm(BaseArm):
    def __init__(self, reward_func) -> None:
        super().__init__()
        self.state_space = {0}
        self.state_transfor_func = lambda x: x  # Bandit只有一个state
        self.reward_func = reward_func

    def step(self, state=None, action=None):
        return self.state_transfor_func(state), self.reward_func.reward(state, action)

    def reset(self):
        return self


