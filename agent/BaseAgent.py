from abc import ABC


class BaseAgent(ABC):

    def __init__(self, agent_num) -> None:
        self.neighbour_nodes = None
        self.agent_num = agent_num
