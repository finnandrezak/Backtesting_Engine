from src.strategy.base import Strategy
from src.event import SignalEvent

class SimpleStrategy(Strategy):
    def calculate_signals(self, event, current_pos):
        if event.type == 'MARKET':
            if current_pos == 0:
                signal = SignalEvent(event.symbol, event.timestamp, 'BUY', event.end_p)
                return signal
            elif current_pos > 0:
                signal = SignalEvent(event.symbol, event.timestamp, 'SELL', event.end_p)
                return signal
        return None
