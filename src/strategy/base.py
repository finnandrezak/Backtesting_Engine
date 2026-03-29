from abc import ABCMeta, abstractmethod

#Base abstract class for all strategies, requires us to include a calculate_signals method in all strategies
class Strategy(metaclass=ABCMeta):
    def __init__(self, max_buys=1):
        self.max_buys = max_buys

    @abstractmethod
    def calculate_signals(self, event, current_pos):
        raise NotImplementedError("diese methode muss überschrieben werden")