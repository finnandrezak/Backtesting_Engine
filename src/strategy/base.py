from abc import ABCMeta, abstractmethod

class Strategy(metaclass=ABCMeta):
    def __init__(self, max_buys=1):
        self.max_buys = max_buys

    @abstractmethod
    def calculate_signals(self, event, current_pos):
        raise NotImplementedError("Method must be implemented")
