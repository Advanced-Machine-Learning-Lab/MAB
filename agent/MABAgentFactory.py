from agent import MABAgent


"""
MABAgentFactory提供静态方法get_agent_list(round_num)

get_agent_list()只需要传入round_num，然后根据本地配置文件、生成多个Agent

其中配置文件包括如下：
1、Agent之间边的关系(edges.txt) 每条记录表示一条带权有向边(u, v, w)
2、每个arm的分布(arms.txt) 由于是Bernoulli分布，每条记录表示一个arm的真实均值。
3、每个Agent的属性(agents.csv)（Agent的序号agent_index、训练轮数round_num、决策子集arms、邻居节点） 每条记录表示一个agent的信息。

最终get_agent_list()会返回agent_num(agent数量)、agents(包含各个Agent的列表)、edges(边的信息)、neighbour_nodes(邻居节点的信息)
"""


class MABAgentFactory(object):
    @staticmethod
    def get_agent_list(round_num=100):
        edges = []
        with open('../data/edges.txt') as f:
            lines = f.readlines()
            for line in lines:
                u, v, w = line.replace('\n', '').split(' ')
                edges.append((int(u), int(v), int(w)))
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
