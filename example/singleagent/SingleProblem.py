from abc import ABC

from agent import BaseProblem


class SingleProblem(BaseProblem, ABC):
    def __init__(self, round_num):
        self.num = None
        self.round_num = round_num
