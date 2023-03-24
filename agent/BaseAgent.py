class BaseAgent(object):

    def __init__(self, neighbour_nodes, agent_num) -> None:
        self.neighbour_nodes = neighbour_nodes
        self.agent_num = agent_num
