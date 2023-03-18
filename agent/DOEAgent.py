import numpy as np
from .Agent import BaseAgent


class DOEAgent(BaseAgent):
    def __init__(self, arm_number, agent_number) -> None:
        super().__init__(arm_number, agent_number)

    # 更新agent_j自身状态
    # arm_sample_nums[agent_j][arm_i]: agent_j pull arm_i的次数
    # arm_rewards[agent_j][arm_i]: agent_j pull arm_i获得的奖励
    # arm_means[agent_j][arm_i]: agent_j对arm_i的均值
    # ind_rew: agent_j的reward
    def update_self_state(self, agent_j, arm_i, reward):
        self.arm_sample_nums[agent_j][arm_i] += 1
        self.arm_rewards[agent_j][arm_i] += reward
        self.arm_means[agent_j][arm_i] = self.arm_rewards[agent_j][arm_i] / self.arm_sample_nums[agent_j][arm_i]
        self.ind_rew += reward

    # 交换两个agent的信息（完成一次通信）: swap(agent_j, agent_jp)
    def update_state(self, agent_jp, arm_i, reward, sample_num):
        self.arm_sample_nums[agent_jp][arm_i] = sample_num
        self.arm_rewards[agent_jp][arm_i] = reward
        self.arm_means[agent_jp][arm_i] = self.arm_rewards[agent_jp][arm_i] / self.arm_sample_nums[agent_jp][arm_i]

    def update_arm_mean(self, arm_i, mean):
        self.arm_mean[arm_i] = mean

    def update_mean_of_agent(self, agent_j, arm_i):
        self.arm_means[agent_j][arm_i] = self.arm_rewards[agent_j][arm_i] / self.arm_sample_nums[agent_j][arm_i]

    def get_mean_of_agent_arm(self, agent_j, arm_i):
        return self.arm_means[agent_j][arm_i]

    def get_sn_of_agent_arm(self, agent_j, arm_i):
        return self.arm_sample_nums[agent_j][arm_i]

    def get_rw_of_agent_arm(self, agent_j, arm_i):
        return self.arm_rewards[agent_j][arm_i]