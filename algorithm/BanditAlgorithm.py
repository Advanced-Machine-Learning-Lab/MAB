import numpy as np
from algorithm import BaseAlgorithm

# from tqdm import trange


class BanditAlgorithm(BaseAlgorithm):
    def __init__(self, neighbour_nodes, agent_num, arm_num, round_num, arms, arms_distribution):
        BaseAlgorithm.__init__(self, neighbour_nodes, agent_num, arm_num, round_num, arms, arms_distribution)

    # 判断是否通信
    def is_communication(self):
        return False

    # 计算置信区间
    def confidence_interval(self, agent_index, delta):
        sample_nums = np.array([self.arms_sample_nums[agent_index][agent_index][i] for i in self.arms[agent_index]])
        return np.sqrt(2 * np.log(1 / delta) / sample_nums)

    # arm选择策略，这里使用了UCB
    # 返回每个agent在t时刻pull的arm的index
    def arm_selection(self, t):
        arm_list = []
        for agent_index in range(self.agent_num):
            means = np.array([self.arms_means[agent_index][agent_index][i] for i in self.arms[agent_index]])
            ci = self.confidence_interval(agent_index, 1 / t)
            arm_sub_index = np.argmax(means + ci)
            arm_index = self.arms[agent_index][arm_sub_index]
            arm_list.append(arm_index)
        return arm_list

    # 定义算法的主流程
    def main(self):
        # 初始化UCB 所有agent对决策集内的arm都pull一次
        for agent_index in range(self.agent_num):
            for arm_index in self.arms[agent_index]:
                self._run(agent_index, arm_index)

        for t in range(1, 1 + self.round_num):
            # t时刻，arm_selection: Simulator内所有agent对决策集内的arm进行选择
            # agent_run_t : 每个agent可以pull的次数
            agent_run_t = [1] * self.agent_num
            self.run(t, agent_run_t, self.arm_selection(t))
            if self.is_communication():
                # 通信定义：每个agent向邻居节点发送信息
                for agent_index in range(self.agent_num):
                    for nei_agent_index in self.neighbour_nodes[agent_index]:
                        self.arms_rewards[nei_agent_index][agent_index] = self.arms_rewards[agent_index][agent_index]
                        self.arms_sample_nums[nei_agent_index][agent_index] = self.arms_sample_nums[agent_index][
                            agent_index]
                self.update_state(t)

        for agent_index in range(self.agent_num):
            print(f'agent:{agent_index}, arm_means:{self.arms_means[agent_index][agent_index]}')


if __name__ == '__main__':
    round_num = 10000
    agent_num = 3
    arm_num = 4
    arms = [[0, 1, 2], [1, 2, 3], [0, 3]]
    neighbour_nodes = [[1, 2], [], [0, 1]]
    arms_distribution = [0.1, 0.3, 0.6, 0.9]

    algo = BanditAlgorithm(neighbour_nodes, agent_num, arm_num, round_num, arms, arms_distribution)
    algo.main()
