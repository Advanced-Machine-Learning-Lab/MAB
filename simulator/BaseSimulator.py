import numpy as np

from agent import MMAB


class BaseSimulator(MMAB):
    def __init__(self, neighbour_nodes, agent_num, arm_num, round_num, arms, arms_distribution):
        super().__init__(neighbour_nodes, agent_num, arm_num, round_num, arms, arms_distribution)
        self.arms_means = np.zeros((self.agent_num, self.agent_num, self.arm_num))
        self.arms_rewards = np.zeros((self.agent_num, self.agent_num, self.arm_num))
        self.arms_sample_nums = np.zeros((self.agent_num, self.agent_num, self.arm_num))

    def _run(self, agent_index, arm_index):
        reward = self.pull(arm_index)
        self.arms_rewards[agent_index][agent_index][arm_index] += reward
        self.arms_sample_nums[agent_index][agent_index][arm_index] += 1
        self.arms_means[agent_index][agent_index][arm_index] = self.arms_rewards[agent_index][agent_index][arm_index] / self.arms_sample_nums[agent_index][agent_index][arm_index]

    def run(self, t, agent_run_t, arms):
        for agent_index in range(self.agent_num):
            run_times = agent_run_t[agent_index]
            for _ in range(run_times):
                self._run(agent_index, arms[agent_index])

    def update_state(self, t):
        for agent_index in range(self.agent_num):
            for nei_agent_index in range(self.agent_num):
                if agent_index == nei_agent_index:
                    continue
                self.arms_rewards[agent_index][agent_index] += self.arms_rewards[agent_index][nei_agent_index]
                self.arms_sample_nums[agent_index][agent_index] += self.arms_sample_nums[agent_index][nei_agent_index]
            for arm_index in self.arms[agent_index]:
                self.arms_means[agent_index][agent_index][arm_index] = self.arms_rewards[agent_index][agent_index][arm_index] / self.arms_sample_nums[agent_index][agent_index][arm_index]