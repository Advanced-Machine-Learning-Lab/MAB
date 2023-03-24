class BaseProblem(object):
    def __init__(self, arm_num, round_num):
        self.arm_num = arm_num
        self.round_num = round_num

        self.arms = None  # 决策集子集
        self.arms_means = None  # 对决策集分布的估计
        self.arms_rewards = None  # 累计奖励
        self.arms_distribution = None  # 总的决策集真实分布
        self.arms_sample_nums = None  # 对决策集的采样次数
