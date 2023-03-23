class BasePolicy:
    def __init__(self, agent, arm_number) -> None:
        self.agent = agent
        self.arm_number = arm_number

    def select_arm(self):
        return 0

    def is_communicated(self, args):
        return True
