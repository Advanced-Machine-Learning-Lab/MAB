import numpy as np

from communication import Communication


class DOECommunication(Communication):
    def __init__(self, agents: list) -> None:
        super().__init__(agents)

    def run(self, arm_i):
        sn_total = 0.0
        rw_total = 0.0
        for j in range(self.agent_number):
            sn_j = self.agents[j].get_sn_of_agent_arm(j, arm_i)  # agent_j sample arm_i的次数
            rw_j = self.agents[j].get_rw_of_agent_arm(j, arm_i)  # agent_j 在arm_i上的reward
            for j_prime in range(self.agent_number):
                if j == j_prime:
                    continue
                sn_jp = self.agents[j_prime].get_sn_of_agent_arm(j_prime, arm_i)  # agent_jp sample arm_i的次数
                rw_jp = self.agents[j_prime].get_rw_of_agent_arm(j_prime, arm_i)  # agent_jp 在arm_i上的reward

                self.agents[j].update_state(j_prime, arm_i, rw_jp, sn_jp)
                self.agents[j_prime].update_state(j, arm_i, rw_j, sn_j)
            sn_total += sn_j
            rw_total += rw_j

        common_mean = rw_total / sn_total

        for j in range(self.agent_number):
            for j_prime in range(self.agent_number):
                self.agents[j].update_mean_of_agent(j_prime, arm_i)

        return len(self.agents), common_mean
