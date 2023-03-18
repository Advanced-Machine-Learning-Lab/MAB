from agent.DOEAgent import DOEAgent
from policy.DOEPolicy import DOEPolicy
from arm.arm import BanditArmFactory
from simulator.DOESimulator import DOESimulator
from communication.DOECommunication import DOECommunication

import numpy as np


class DOEMAB:
    def __init__(self, simulation_times, agent_number, arm_number, T, alpha, beta, delta) -> None:
        self.simulation_times = simulation_times
        self.agent_number = agent_number
        self.arm_number = arm_number
        self.T = T
        self.alpha = alpha
        self.beta = beta
        self.delta = delta
        self.agents = None
        self.policies = None
        self.arms = None
        self.communication = None
        self.arm_real_means = np.linspace(1, 99, self.arm_number) / 100
        self.opt_arm_mean = self.arm_real_means[-1]
        self.init_static()

    def init_static(self):
        self.agents = [DOEAgent(self.arm_number, self.agent_number) for _ in range(self.agent_number)]
        self.policies = [DOEPolicy(agent, self.arm_number) for agent in self.agents]
        self.arms = BanditArmFactory.get(self.arm_real_means)
        self.communication = DOECommunication(self.agents)

    def reset(self):
        self.init_static()

    def run(self):
        group_reward_avg = []
        ind_rew_ave = []
        for _ in range(self.simulation_times):
            group_regrets = []
            ind_regrets = []

            # 定义Simulator
            doe_simulator = DOESimulator(self.agents, self.arms, self.policies, self.communication, self.T, self.alpha,
                                         self.beta, self.delta)
            for ret in doe_simulator:
                t, group_reward, communication_times, candidate_set = ret['t'], ret['group_reward'], \
                    ret['communication_times'], ret['candidate_set']
                ind_reward = ret['ind_rew']
                sample_arm_mean = ret['sample_arm_mean']
                group_regrets.append(t * self.opt_arm_mean * self.agent_number - group_reward)
                ind_regrets.append(t * self.opt_arm_mean - ind_reward)
                if t % 1000 == 0:
                    print(f"com:{communication_times}, "
                          f"group_regret:{group_regrets[-1]}, "
                          f"candidate_set:{candidate_set} sample_mean:{sample_arm_mean}")
            group_reward_avg.append(group_regrets)
            ind_rew_ave.append(ind_regrets)
            self.reset()

    def __str__(self):
        return f"DOE MAB. {self.agent_number} agents, {self.arm_number} arms."


if __name__ == '__main__':
    mab = DOEMAB(2, 10, 10, 5000, 0.1, 2, 1 / 5000)
    print(mab)
    mab.run()
