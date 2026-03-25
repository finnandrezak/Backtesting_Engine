from src.event import MarketEvent
from src.event import OrderEvent
from src.event import FillEvent

"""
Portfolio Class: keeps track of cash and assets/total holdings
"""
class Portfolio:
    def __init__(self, stop_loss_pct, initial_capital=1000000.0):
        self.initial_capital = initial_capital
        self.current_cash = initial_capital
        self.stop_loss_pct = stop_loss_pct
        self.holdings = {}
        self.entry_prices = {}
        self.latest_prices = {}
        self.equity_curve = []

    #keeps prices and equity updated
    def update_market(self, event):
        if event.type == 'MARKET':
            self.latest_prices[event.symbol] = event.end_p
            self.equity_curve.append((event.timestamp, self.get_equity()))

    def check_stop_loss(self, event):
        if event.type == 'MARKET':
            symbol =event.symbol
            price = event.end_p

            if symbol in self.holdings and self.holdings[symbol] > 0:
                entry_price = self.entry_prices.get(symbol, 0)
                if entry_price > 0:
                    price_drop = (entry_price - price) / entry_price

                    if price_drop >= self.stop_loss_pct:
                        print(f"Portfolio: STOP LOSS triggered for {symbol}")
                        return OrderEvent(event.timestamp, symbol, 'MARKET', self.holdings[symbol], 'SELL', price)
        return None

    #handles signal events from strategy
    def update_signal(self, event, broker):
        if event.type == 'SIGNAL':
            direction = event.signal_type
            target_price = event.suggested_price
            symbol = event.symbol
            quantity = 0
            commission = broker.commission

            if direction == 'SELL':
                quantity = self.holdings.get(symbol, 0)
                if quantity <= 0:
                    print(f"Portfolio: SELL refused, not enough {symbol} in the portfolio!")
                    return None

            elif direction == 'BUY':

                current_equity= self.get_equity()
                risk_per_trade = current_equity *0.10
                quantity = int(risk_per_trade / target_price)
                total_cost = (quantity * target_price) + commission

                if self.current_cash < total_cost:
                   quantity = int((self.current_cash - commission) /target_price)

                if quantity <= 0:
                    print(f"not enough cash to buy even one share of {symbol}")
                    return None

            order = OrderEvent(event.timestamp, event.symbol, 'MARKET', quantity, direction, target_price)
            print(f"portfolio: order created! {direction} {quantity} {event.symbol}")
            return order

        return None

    #calculates order fills
    def update_fill(self, fill_event):
        trade_pps = fill_event.fill_cost
        quantity = fill_event.quantity
        trade_cost = trade_pps * quantity
        fee = fill_event.commission
        symbol = fill_event.symbol

        if fill_event.direction == 'BUY':
            current_qty = self.holdings.get(symbol, 0)
            if current_qty == 0:
                self.entry_prices[symbol] = trade_pps

            else:
                total_cost = (current_qty *self.entry_prices.get(symbol, trade_pps)) + trade_cost
                new_total_qty = current_qty + quantity
                self.entry_prices[symbol] = total_cost / new_total_qty

            self.current_cash -= (trade_cost + fee)
            self.holdings[symbol] = current_qty + fill_event.quantity

        elif fill_event.direction == 'SELL':
            self.current_cash += (trade_cost - fee)
            self.holdings[symbol] = self.holdings.get(symbol, 0) - fill_event.quantity

            if self.holdings[symbol] <= 0:
                self.entry_prices[symbol] = 0.0

        print(
            f"Portfolio update: {fill_event.symbol}, holdings: {self.holdings[fill_event.symbol]} , cash: {self.current_cash:.2f}$")

    #helping method to get total value of portfolio
    def get_equity(self):
        total_holdings = 0.0
        total_holdings += self.current_cash

        for symbol, quantity in self.holdings.items():
            current_price = self.latest_prices.get(symbol, 0.0)
            total_holdings += (quantity * current_price)

        return round(total_holdings, 2)

    def liquidate_all_positions(self, broker):
        if not self.equity_curve:
            print("Portfolio: nothing to liquidate, no market data received yet")
            return

        print("=== Portfolio: Final Liquidation Started ====")
        for symbol in list(self.holdings.keys()):
            quantity = self.holdings.get(symbol, 0)

            if quantity > 0:
                last_price = self.latest_prices.get(symbol, 0.0)
                last_time = self.equity_curve[-1][0]
                final_fill = FillEvent(last_time, symbol, quantity, 'SELL', last_price, broker.commission)
                self.update_fill(final_fill)


    def get_statistics(self, benchmark_curve):
        if not self.equity_curve:
            return None

        equity_values = [val for _, val in self.equity_curve]
        initial = self.initial_capital
        final = equity_values[-1]


        return_pct = ((final - initial ) /initial) * 100

        max_drawdown = 0.0
        peak = equity_values[0]
        for val in equity_values:
            if val > peak:
                peak = val
            drawdown = (peak - val) / peak

            if drawdown > max_drawdown:
                max_drawdown = drawdown

        b_initial = benchmark_curve[0][1]
        b_final = benchmark_curve[-1][1]
        benchmark_return = ((b_final - b_initial) / b_initial) * 100


        return {
            'initial': initial,
            'final': final,
            'return_pct': return_pct,
            'max_drawdown': max_drawdown * 100, #(in percentile)
            'benchmark_return': benchmark_return
        }

