from strategy.base import Strategy
from src.event import SignalEvent

"""
classic and simple Moving average Strategy:
calculates moving average and compares it with current price, 
doesn't hold positions bigger than 500 shares to combat volatility
"""


class SMA_Strategy(Strategy):
    def __init__(self):
        self.history = {}
        self.short_lookback = 20
        self.long_lookback = 100
        self.max_buys = 3
        self.buy_counter = {}

    def calculate_signals(self, event, current_pos):
        if event.type == 'MARKET':
            symbol = event.symbol
            price = event.end_p

            if symbol not in self.history:
                self.history[symbol] = []
                self.buy_counter[symbol] = 0

            if current_pos == 0:
                self.buy_counter[symbol] = 0

            self.history[symbol].append(price)

            if len(self.history[symbol]) >= self.short_lookback:
                if len(self.history[symbol]) > self.long_lookback:
                    self.history[symbol].pop(0)

                short_avg = sum(self.history[symbol][-self.short_lookback:]) / self.short_lookback
                long_avg = sum(self.history[symbol]) / self.long_lookback

                if price > short_avg and price > long_avg:
                    if self.buy_counter[symbol] < self.max_buys:
                        self.buy_counter[symbol] += 1
                        return SignalEvent(symbol, event.timestamp, 'BUY', price)
                elif price < short_avg and current_pos > 0:
                    return SignalEvent(symbol, event.timestamp, 'SELL', price)


        return None
