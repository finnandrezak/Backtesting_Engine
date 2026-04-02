from src.event import FillEvent

class Broker:
    def __init__(self, commission=9.90, slippage_pct=0.0001):
        self.commission = commission
        self.slippage_pct = slippage_pct

    def execute_order(self, event):
        if event.type == 'ORDER':
            slippage = event.target_price * self.slippage_pct
            if event.direction == 'BUY':
                fill_price = event.target_price + slippage
            else:
                fill_price = event.target_price - slippage
            print(f"Order filled: {event.symbol} at ${fill_price:.2f}")
            return FillEvent(
                event.timestamp,
                event.symbol,
                event.quantity,
                event.direction,
                fill_price,
                self.commission

            )

