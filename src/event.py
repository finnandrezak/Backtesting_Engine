#base class for events
class Event:
    pass

class MarketEvent(Event):
    def __init__(self, symbol, timestamp, open_p, high_p, low_p, end_p, volume):
        self.type = 'MARKET'
        self.symbol = symbol
        self.timestamp = timestamp
        self.open_p = open_p
        self.high_p = high_p
        self.low_p = low_p
        self.end_p = end_p
        self.volume = volume


class SignalEvent(Event):
    def __init__(self, symbol, datetime, signal_type, suggested_price):
        self.type = 'SIGNAL'
        self.symbol = symbol
        self.datetime = datetime
        self.signal_type = signal_type
        self.suggested_price = suggested_price

class OrderEvent(Event):
    def __init__(self, symbol, order_type, quantity, direction, target_price):
        self.type = 'ORDER'
        self.symbol = symbol
        self.order_type = order_type
        self.quantity = quantity
        self.direction = direction
        self.target_price = target_price

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

