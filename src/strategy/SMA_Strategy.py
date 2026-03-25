from strategy.base import Strategy
from src.event import SignalEvent
"""
classic and simple Moving average Strategy:
calculates moving average and compares it with current price
"""

class SMA_Strategy (Strategy):
    def __init__(self):
        self.history = {}
        self.lookback = 20
        self.stop_loss_pct = 0.2

    def calculate_signals(self, event):
        if event.type == 'MARKET':
            symbol = event.symbol
            price =event.end_p

            if symbol not in self.history:
                self.history[symbol] = []

            self.history[symbol].append(price)

            if len(self.history[symbol]) > self.lookback:

                self.history[symbol].pop(0)
                avg_price =sum(self.history[symbol]) /self.lookback

                if price > avg_price:
                    return SignalEvent(symbol, event.timestamp, 'BUY', price)
                elif price < avg_price:
                    return SignalEvent(symbol, event.timestamp, 'SELL', price)

        return None


