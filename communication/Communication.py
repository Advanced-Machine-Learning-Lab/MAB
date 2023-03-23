class Communication:
    def __init__(self, agents: list) -> None:
        self.agents = agents
        self.agent_number = len(self.agents)

    def run(self, arm_i):
        raise NotImplementedError
