from agent import BaseAgent, Event, Message, Router

from example.singleagent import SingleAlgorithm
from example.singleagent import SingleProblem


class SingleAgent(BaseAgent, SingleProblem, SingleAlgorithm, Event, Message, Router):
    def __init__(self, agent_num, agent_index, neighbour_node, round_num):
        BaseAgent.__init__(self, agent_num)
        SingleProblem.__init__(self, round_num)
        SingleAlgorithm.__init__(self)
        Event.__init__(self)
        Message.__init__(self)
        Router.__init__(self)

        self.neighbour_node = neighbour_node

        self.num = 0
        self.agent_index = agent_index
        self.edges = None
        self.t = 1

    def __str__(self):
        return f'[t:{self.t}, agent_index:{self.agent_index}, neighbour_node:{self.neighbour_node}, num:{self.num}]'


if __name__ == '__main__':
    agent = SingleAgent(1, 1, [], 1)
