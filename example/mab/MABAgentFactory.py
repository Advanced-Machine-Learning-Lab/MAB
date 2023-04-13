import pandas as pd
import os

from example.mab import MABAgent


class MABAgentFactory(object):
    @staticmethod
    def get_agent_list(read_edges=True, read_arms=True, read_agents=True, round_num=100, prefix_path='./mab/data'):
        edges = {}
        if read_edges:
            with open(os.path.join(prefix_path, 'edges.txt')) as f:
                lines = f.readlines()
                for line in lines:
                    u, v, w = line.replace('\n', '').split(' ')
                    u, v, w = int(u), int(v), int(w)
                    if u not in edges:
                        d = {v: w}
                        edges[u] = d
                    else:
                        if v not in edges[u]:
                            edges[u][v] = w
                        else:
                            edges[u][v] = min(edges[u][v], w)
        arms_distribution = []
        if read_arms:
            with open(os.path.join(prefix_path, 'arms.txt')) as f:
                lines = f.readlines()
                for line in lines:
                    arms_distribution.append(float(line.replace('\n', '')))
        arms_num = len(arms_distribution)
        agents = []
        neighbour_nodes = []
        agent_num = 0
        if read_agents:
            agent_csv = pd.read_csv(os.path.join(prefix_path, 'agents.csv'))
            agent_num = agent_csv.shape[0]
            for i in range(agent_num):
                agent_index = int(agent_csv.iloc[i][0])
                arms = agent_csv.iloc[i][1].split(';')
                arms = [int(arm) for arm in arms]
                neighbour_node = agent_csv.iloc[i][2].split(';')
                neighbour_node = [int(node) for node in neighbour_node]
                agents.append(MABAgent(agent_num=agent_num,
                                       agent_index=agent_index,
                                       round_num=round_num,
                                       arm_num=arms_num,
                                       arms=arms,
                                       arms_distribution=arms_distribution))
                neighbour_nodes.append(neighbour_node)
        for agent in agents:
            agent.update()


        return agent_num, agents, edges, neighbour_nodes
