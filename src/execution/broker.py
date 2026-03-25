from src.event import FillEvent

"""
Broker-class, turns Order Events into Fill Events i.e. executes the order, and adds commission logic
"""

class Broker:
    def __init__(self, commission=9.90, slippage_pct=0.0001 ):
        self.commission = commission
        self.slippage_pct = slippage_pct


    #executes order events
    def execute_order(self, event):
        if event.type == 'ORDER':
            slippage = event.target_price * self.slippage_pct
            if event.direction == 'BUY':
                fill_price = event.target_price + slippage
            else:
                fill_price = event.target_price - slippage
            print(f"Broker: order filled! {event.symbol} at {fill_price} $")
            return FillEvent(
                event.timestamp,
                event.symbol,
                event.quantity,
                event.direction,
                fill_price,
                self.commission

            )

