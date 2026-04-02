import numpy as np
from src.strategy.base import Strategy
from src.event import SignalEvent

class Regime_Switch_Strategy(Strategy):
    def __init__(self, lookback=50, regime_window=30, z_threshold=1.2, r2_threshold=0.4):
        super().__init__()
        self.history = {}
        self.lookback = lookback
        self.regime_window = regime_window
        self.z_threshold = z_threshold
        self.r2_threshold = r2_threshold
        self.max_buys = 1
        self.buy_counter = {}

    def calc_r_squared(self, y):
        x = np.arange(len(y))
        slope, intercept = np.polyfit(x, y, 1)
        y_pred = slope * x + intercept

        ss_res = np.sum((y - y_pred)**2)
        ss_tot = np.sum((y - np.mean(y))**2)

        if ss_tot == 0:
            return 0, slope

        r2 = 1 - (ss_res / ss_tot)
        return r2, slope

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

            if len(self.history[symbol]) >= self.lookback:
                if len(self.history[symbol]) > self.lookback:
                    self.history[symbol].pop(0)

                prices = np.array(self.history[symbol])

                regime_prices = prices[-self.regime_window:]
                r2, slope = self.calc_r_squared(regime_prices)

                mean_price = np.mean(prices)
                std_dev = np.std(prices)

                z_score = (price - mean_price) / std_dev if std_dev > 0 else 0

                short_sma = np.mean(prices[-10:])

                if r2 < self.r2_threshold:
                    if z_score < -self.z_threshold and self.buy_counter[symbol] < self.max_buys:
                        self.buy_counter[symbol] += 1
                        print(f"Z-score BUY at {price:.2f}")
                        return SignalEvent(symbol, event.timestamp, 'BUY', price)

                    elif z_score >= 0 and current_pos > 0:
                        print(f"Mean reversion SELL at {price:.2f}")
                        return SignalEvent(symbol, event.timestamp, 'SELL', price)

                else:
                    if slope > 0 and price > short_sma and self.buy_counter[symbol] < self.max_buys:
                        self.buy_counter[symbol] += 1
                        print(f"Momentum BUY at {price:.2f}")
                        return SignalEvent(symbol, event.timestamp, 'BUY', price)

                    elif (slope < 0 or price < short_sma) and current_pos > 0:
                        print(f"Trend break SELL at {price:.2f}")
                        return SignalEvent(symbol, event.timestamp, 'SELL', price)

        return None