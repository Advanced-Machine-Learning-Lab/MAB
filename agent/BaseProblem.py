from abc import ABC, abstractmethod


class BaseProblem(ABC):
    # BaseProblem不定义任何问题属性

    @abstractmethod
    def __init__(self):
        pass

