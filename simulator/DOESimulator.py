import numpy as np
from simulator import BaseSimulator
from communication import DOECommunication

class DOESimulator(BaseSimulator):
    # 传入agent、arms和policy均为实例的引用
    def __init__(self, agents: list, arms: list, policies: list, communication: DOECommunication, T: int, alpha: float, beta: float, delta: float) -> None:
        super().__init__(agents, arms, policies, communication, T)
        self.alpha = alpha
        self.beta = beta
        self.delta = delta
        self.nt_of_arms = np.zeros(self.arms_number)  # pull arm的次数
        self.ei_last = np.array(
            [self.alpha * np.sqrt(np.log2(2.0 / self.delta) / (2.0 * self.agent_number)) for _ in range(self.arms_number)])
        self.common_means = np.zeros(self.arms_number)
        self.group_reward = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.t < self.T:
            # 是否通信
            is_communicated_flag = False

            # 遍历每一个agent，选择一个arm去pull
            # policy: select an arm_i
            # DEA的策略是Robin-Round，固定选取policy[0]即可
            arm_i = self.policies[0].select_arm()
            for j in range(self.agent_number):
                # pull arm_i
                _, reward = self.arms[arm_i].step()
                # 更新agent_j对arm_i的reward、pull的次数以及mean
                self.agents[j].update_self_state(j, arm_i, reward)

            self.nt_of_arms[arm_i] += self.agent_number  # 记录pull当前arm的次数

            ei = self.estimation_interval(arm_i)  # 计算当前arm的estimate interval
            for j in range(self.agent_number):
                if self.beta * ei < self.ei_last[arm_i]:
                    self.ei_last[arm_i] = ei
                if self.policies[j].is_communicated({"arm_i": arm_i,
                                                     "common_mean": self.common_means[arm_i],
                                                     "ei": ei,
                                                     "t": self.t}):
                    is_communicated_flag = True
                    break

            if is_communicated_flag:
                communication_times, common_mean = self.communication.run(arm_i)
                self.communication_times += communication_times
                self.common_means[arm_i] = common_mean

            # 计算mu(j)
            for j in range(self.agent_number):
                rw_of_all_agent = 0.0
                mt_j_j = self.agents[j].get_mean_of_agent_arm(j, arm_i)
                sn_j_j = self.agents[j].get_sn_of_agent_arm(j, arm_i)
                for j_prime in range(self.agent_number):
                    mt_j_jp = self.agents[j].get_mean_of_agent_arm(j_prime, arm_i)
                    sn_j_jp = self.agents[j].get_sn_of_agent_arm(j_prime, arm_i)
                    rw_of_all_agent += mt_j_jp * sn_j_jp + mt_j_j * (sn_j_j - sn_j_jp)

                mean_of_agent = rw_of_all_agent / (sn_j_j * self.agent_number)
                self.agents[j].update_arm_mean(arm_i, mean_of_agent)

            # eliminate_arm
            for j in range(self.agent_number):
                for candidate_arm in range(self.arms_number):
                    if self.policies[0].candidate_set[candidate_arm] == 0:
                        continue
                    ci_cand = self.confidence_interval(self.nt_of_arms[candidate_arm])
                    mean_cnd = self.agents[j].arm_mean[candidate_arm]
                    for another_arm in range(self.arms_number):
                        if self.policies[0].candidate_set[candidate_arm] == 0:
                            continue
                        if another_arm == candidate_arm or self.policies[0].candidate_set[another_arm] == 0:
                            continue
                        mean_ano = self.agents[j].arm_mean[another_arm]
                        six_alpha_ci = 6.0 * self.alpha * ci_cand
                        if mean_cnd + six_alpha_ci < mean_ano:
                            self.policies[0].candidate_set[candidate_arm] = 0
                            break

            self.group_reward = 0
            for j in range(self.agent_number):
                self.group_reward += self.agents[j].ind_rew

            sample_arm_mean = self.agents[0].arm_means[0:]
            ret = {"t": self.t,
                   "group_reward": self.group_reward,
                   "ind_rew": self.agents[0].ind_rew,
                   "communication_times": self.communication_times,
                   "candidate_set": self.policies[0].candidate_set,
                   "estimate_arm_mean": self.agents[0].arm_mean,
                   "sample_arm_mean": sample_arm_mean}
            self.t += 1
            return ret

        raise StopIteration

    def estimation_interval(self, arm_i):
        nt_of_arm = self.nt_of_arms[arm_i] if self.nt_of_arms[arm_i] > 0 else self.agent_number
        return self.alpha * np.sqrt(np.log2(2.0 / self.delta) / (2.0 * nt_of_arm))

    def confidence_interval(self, num):
        num = 1 if num == 0 else num
        return np.sqrt(np.log2(2.0 / self.delta) / (2.0 * num))