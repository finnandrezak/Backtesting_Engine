import numpy as np
from strategy.base import Strategy
from src.event import SignalEvent

class Regime_Switch_Strategy(Strategy):
    def __init__(self, lookback=50, regime_window=30, z_threshold=1.2, r2_threshold=0.4):
        super().__init__()
        self.history = {}
        self.lookback = lookback
        self.regime_window = regime_window

        # Quant Parameters
        self.z_threshold = z_threshold
        self.r2_threshold = r2_threshold

        # Strict Risk Control: Only 1 position at a time per symbol
        self.max_buys = 1
        self.buy_counter = {}

    def calc_r_squared(self, y):
        """Calculates the R^2 of a linear regression to detect trend strength."""
        x = np.arange(len(y))
        # Fit a 1st degree polynomial (straight line)
        slope, intercept = np.polyfit(x, y, 1)
        y_pred = slope * x + intercept

        # Calculate sum of squares
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

            # Sync strategy state with actual portfolio holdings
            if current_pos <= 0:
                self.buy_counter[symbol] = 0

            self.history[symbol].append(price)

            # Wait for enough data to fill the quantitative lookback window
            if len(self.history[symbol]) >= self.lookback:
                if len(self.history[symbol]) > self.lookback:
                    self.history[symbol].pop(0)

                # Convert to numpy array for fast C-level math operations
                prices = np.array(self.history[symbol])

                # --- 1. REGIME DETECTION ---
                regime_prices = prices[-self.regime_window:]
                r2, slope = self.calc_r_squared(regime_prices)

                # --- 2. STATISTICAL METRICS ---
                mean_price = np.mean(prices)
                std_dev = np.std(prices)

                # Avoid division by zero in perfectly flat markets
                z_score = (price - mean_price) / std_dev if std_dev > 0 else 0

                short_sma = np.mean(prices[-10:]) # Fast momentum tracker

                # ==========================================
                # THE DECISION ENGINE
                # ==========================================

                # REGIME A: SIDEWAYS / CHOPPY MARKET (Low R^2)
                if r2 < self.r2_threshold:

                    # BUY: Price is mathematically heavily oversold (Z < -2.0)
                    if z_score < -self.z_threshold and self.buy_counter[symbol] < self.max_buys:
                        self.buy_counter[symbol] += 1
                        print(f"[QUANT] Sideways Regime: Z-Score BUY at {price:.2f} (Z: {z_score:.2f}, R2: {r2:.2f})")
                        return SignalEvent(symbol, event.timestamp, 'BUY', price)

                    # SELL: Price reverted to the mean (Z >= 0)
                    elif z_score >= 0 and current_pos > 0:
                        print(f"[QUANT] Sideways Regime: Mean-Reversion SELL at {price:.2f}")
                        return SignalEvent(symbol, event.timestamp, 'SELL', price)

                # REGIME B: TRENDING MARKET (High R^2)
                else:

                    # BUY: Trend is UP (slope > 0) and we have short-term momentum
                    if slope > 0 and price > short_sma and self.buy_counter[symbol] < self.max_buys:
                        self.buy_counter[symbol] += 1
                        print(f"Regime: Momentum BUY at {price:.2f} (R2: {r2:.2f})")
                        return SignalEvent(symbol, event.timestamp, 'BUY', price)

                    # SELL: Trend broke OR short-term momentum died
                    elif (slope < 0 or price < short_sma) and current_pos > 0:
                        print(f"Regime: Trend-Break SELL at {price:.2f}")
                        return SignalEvent(symbol, event.timestamp, 'SELL', price)

        return None