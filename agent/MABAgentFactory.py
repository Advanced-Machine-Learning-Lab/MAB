from agent import MABAgent


class MABAgentFactory(object):
    @staticmethod
    def get_agent_list(round_num=100):
        edges = []
        with open('../data/edges.txt') as f:
            lines = f.readlines()
            for line in lines:
                u, v, w = line.replace('\n', '').split(' ')
                edges.append((int(u), int(v), int(w)))
        # print(f'MABAgentFactory edges:{edges}')
        arms_distribution = []
        with open('../data/arms.txt') as f:
            lines = f.readlines()
            for line in lines:
                arms_distribution.append(float(line.replace('\n', '')))
        arms_num = len(arms_distribution)
        agents = []
        import pandas as pd
        agent_csv = pd.read_csv('../data/agents.csv')
        agent_num = agent_csv.shape[0]
        neighbour_nodes = []
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

        return agent_num, agents, edges, neighbour_nodes
