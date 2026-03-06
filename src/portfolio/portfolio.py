from src.event import OrderEvent

class Portfolio:
    def __init__(self, initial_capital=1000000.0):
        self.initial_capital=initial_capital
        self.current_cash = initial_capital
        self.holdings = {}

    def update_signal(self, event):
        if event.type == 'SIGNAL':
            quantity = 100
            direction = event.signal_type

            order = OrderEvent(event.symbol, event.type, quantity, direction)
            print(f"portfolio: order created! {direction} {quantity} {event.symbol}")
            return order
        return None

    def update_fill(self, fill_event):
        cost = fill_event.fill_cost * fill_event.quantity

        self.current_cash -= cost

        if fill_event.symbol in self.holdings:
            self.holdings[fill_event.symbol] += fill_event.quantity
        else:
            self.holdings[fill_event.symbol] = fill_event.quantity
        print(f"Portfolio update: {fill_event.symbol}, holdings: {self.holdings[fill_event.symbol]} , cash: {self.current_cash:.2f}$")