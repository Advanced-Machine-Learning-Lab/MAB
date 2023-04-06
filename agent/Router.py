"""
Router类用于记录Final Agent的内存地址
"""


class Router(object):
    def __init__(self):
        self.addresses = None

    # @property
    # def addresses(self):
    #     return self._addresses
    #
    # @addresses.setter
    # def addresses(self, value: list):
    #     if value is None or len(value) == 0:
    #         self._addresses = None
    #         return
    #     self._addresses = value
