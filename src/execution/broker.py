from src.event import FillEvent

class Broker:
    def __init__(self, ):
        pass

    def execute_order(self, event):
        if event.type == 'ORDER':
            fill_price = event.target_price

            fill_event = FillEvent(
                timestamp= 'NOW',
                symbol = event.symbol,
                quantity = event.quantity,
                direction =event.direction,
                fill_cost = fill_price
            )
            print(f"Broker: order filled! {event.symbol} at {fill_price}")
            return fill_event

