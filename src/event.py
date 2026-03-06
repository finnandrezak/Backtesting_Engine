#base class for events
class Event:
    pass

class MarketEvent(Event):
    def __init__(self):
        self.type = 'MARKET'

class SignalEvent(Event):
    def __init__(self, symbol, datetime, signal_type):
        self.type = 'SIGNAL'
        self.symbol = symbol
        self.datetime = datetime
        self.signal_type = signal_type

class OrderEvent(Event):
    def __init__(self, symbol, order_type, quantity, direction):
        self.type = 'ORDER'
        self.symbol = symbol
        self.order_type = order_type
        self.quantity = quantity
        self.direction = direction

    def print_order(self):
        print(f"Order: symbol = {self.symbol}, Ordertype = {self.order_type},"
              f" quantity = {self.quantity}, direction = {self.direction}")

class FillEvent(Event):
    def __init__(self, timestamp, symbol, quantity, direction, fill_cost, comission=None):
        self.type = 'FILL'
        self.timestamp = timestamp
        self.symbol = symbol
        self.quantity = quantity
        self.direction = direction
        self.fill_cost = fill_cost
        self.comission = comission if comission is not None else 0.0

