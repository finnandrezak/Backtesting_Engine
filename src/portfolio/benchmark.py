"""
Benchmark: a simple "Buy-and-Hold" Benchmark, in order to better review our performance
"""

class Benchmark:
    def __init__(self, initial_capital):
        self.initial_capital = initial_capital
        self.equity_curve = []
        self.first_prices = {}
        self.current_prices = {}

    def update(self, timestamp, symbol, current_price):
        if symbol not in self.first_prices:
            self.first_prices[symbol] = current_price

        self.current_prices[symbol] = current_price

        num_symbols = len(self.first_prices)
        if num_symbols > 0:
            total_value = 0
            capital_per_symbol = self.initial_capital /num_symbols

            for s in self.first_prices:
                s_price = self.current_prices.get(s, self.first_prices[s])
                shares = capital_per_symbol / self.first_prices[s]
                total_value += shares * s_price

            self.equity_curve.append((timestamp, total_value))

    def get_curve(self):
        return self.equity_curve