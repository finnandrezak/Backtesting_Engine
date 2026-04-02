import numpy as np
from src.strategy.base import Strategy
from src.event import SignalEvent

class Advanced_Volatility_Strategy(Strategy):
    def __init__(self, short_period=14, long_period=50, rsi_period=14):
        super().__init__()
        self.history = {}
        self.short_period = short_period
        self.long_period = long_period
        self.rsi_period = rsi_period
        self.max_buys = 3
        self.buy_counter = {}

    def calculate_rsi(self, prices):
        if len(prices) < self.rsi_period + 1:
            return 50
        deltas = np.diff(prices)
        up = np.sum(deltas[deltas >= 0][-self.rsi_period:]) / self.rsi_period
        down = -np.sum(deltas[deltas < 0][-self.rsi_period:]) / self.rsi_period
        if down == 0: return 100
        rs = up / down
        return 100. - (100. / (1. + rs))

    def calculate_signals(self, event, current_pos):
        if event.type == 'MARKET':
            symbol = event.symbol
            price = event.end_p

            if symbol not in self.history:
                self.history[symbol] = []
                self.buy_counter[symbol] = 0

            if current_pos <= 0:
                self.buy_counter[symbol] = 0

            self.history[symbol].append(price)

            if len(self.history[symbol]) >= self.long_period:
                if len(self.history[symbol]) > self.long_period:
                    self.history[symbol].pop(0)

                prices = np.array(self.history[symbol])

                alpha = 2 / (self.long_period + 1)
                ema_long = prices[0]
                for price in prices:
                    ema_long = (price * alpha) + (ema_long * (1 - alpha))

                std = np.std(prices[-self.short_period:])
                upper_band = ema_long + (2 * std)
                rsi = self.calculate_rsi(prices)

                lookback_5 = prices[-5]
                price_change_pct = (price - lookback_5) / lookback_5

                if price > upper_band and price > ema_long:
                    if 50 < rsi < 65 and price_change_pct > 0.02:
                        if self.buy_counter[symbol] < self.max_buys:
                            self.buy_counter[symbol] += 1
                            print(f"High conviction BUY at {price:.2f} (RSI: {rsi:.1f})")
                            return SignalEvent(symbol, event.timestamp, 'BUY', price)

                elif (price < ema_long or rsi > 75) and current_pos > 0:
                    print(f"Exit signal at {price:.2f} (RSI: {rsi:.1f})")
                    return SignalEvent(symbol, event.timestamp, 'SELL', price)

        return None