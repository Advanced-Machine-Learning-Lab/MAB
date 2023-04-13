import os
import pandas as pd

from example.singleagent.SingleAgent import SingleAgent


class SingleAgentFactory(object):
    # 读取配置文件并生成Agent
    @staticmethod
    def get_agent_list(read_edges=True, read_arms=True, read_agents=True, round_num=100, prefix_path='../example/singleagent/data'):
        edges = {}
        if read_edges:
            # pd.read_csv('')
            print(f'dir:{os.getcwd()}')
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

        agents = []
        neighbour_nodes = []
        agent_num = 0
        if read_agents:
            agent_csv = pd.read_csv(os.path.join(prefix_path, 'agents.csv'))
            agent_num = agent_csv.shape[0]
            for i in range(agent_num):
                agent_index = int(agent_csv.iloc[i][0])
                neighbour_node = str(agent_csv.iloc[i][1]).split(';')
                neighbour_node = [int(node) for node in neighbour_node]
                agents.append(
                    SingleAgent(
                        agent_num=agent_num,
                        neighbour_node=neighbour_node,
                        agent_index=agent_index,
                        round_num=round_num)
                )
                neighbour_nodes.append(neighbour_node)
        agents[0].set_event_time('message_sending', 1)
        return agent_num, agents, edges, neighbour_nodes
