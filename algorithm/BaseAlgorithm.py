from abc import ABCMeta, abstractmethod


"""
BaseAlgorithm是一个「抽象类」
必须通过继承、实现内部的所有「方法」

Python中定义抽象类：1、继承ABC 2、指定元类为ABCMeta

定义抽象方法 加上装饰器@abstractmethod
"""


class BaseAlgorithm(object, metaclass=ABCMeta):
    @abstractmethod
    def __init__(self):
        pass

    """
    update()
    最终的Agent会继承Algorithm等类，这个Agent实际上是可以独立运行的。
    Algorithm在此处定义update()函数，该函数被调用时，Agent会根据当前需要做的动作（pull arm、通信等等），进行相应的更新，我们称之为「update」
    Simulator可以协调多个Final Agent
    """

    @abstractmethod
    def update(self) -> int:
        pass
