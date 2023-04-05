from agent.BaseAgent import BaseAgent


class BanditAgent(BaseAgent):
    def __init__(self, agent_num):
        super().__init__(agent_num)