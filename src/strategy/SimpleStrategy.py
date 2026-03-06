from strategy.base import Strategy
from src.event import SignalEvent

#first test for a strategy implemented, simply buys as soon as we get a market signal

class SimpleStrategy(Strategy):
    def calculate_signals(self, event):
        if event.type == 'MARKET':
            "strategy: recognised market event, setting buy order: "
            signal =SignalEvent('AAPL', '2026.03.06', 'BUY')
            return signal
        return None
