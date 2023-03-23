from arm.Rward import BanditReward
from arm.Arm import BanditArm


# 根据arm的reward分布获取BanditArm
# reward为Bernoulli分布，所以需要指定arm的mean
class BanditArmFactory:
    @staticmethod
    def get(arm_distribution):
        bandit_reward_func = [BanditReward(x) for x in arm_distribution]
        return [BanditArm(reward_func) for reward_func in bandit_reward_func]
