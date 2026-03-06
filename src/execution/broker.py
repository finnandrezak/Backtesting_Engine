from src.event import FillEvent

class Broker:
    def execute_order(self, event):
        if event.type == 'ORDER':
            fill_event = FillEvent(
                timestamp='NOW',
                symbol=event.symbol,
                quantity=event.quantity,
                direction =event.direction,
                fill_cost=150.0
            )
            print(f"Broker: order filled! {event.symbol} at 150.0")
            return fill_event

