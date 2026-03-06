from abc import ABCMeta, abstractmethod

#Base abstract class for all strategies, requires us to include a calculate_signals method in all strategies
class Strategy(metaclass=ABCMeta):


    @abstractmethod
    def calculate_signals(self, event):
        raise NotImplementedError("diese methode muss überschrieben werden")