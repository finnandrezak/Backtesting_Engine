import queue
from data.handler import CSVHandler
from execution.broker import Broker
from strategy.SimpleStrategy import SimpleStrategy
from portfolio.portfolio import Portfolio


# this is were we actually start our simulation of the market. first we start an event queue aswell as a new data handler with our CSV as the input

def main():
    events = queue.Queue()
    data_handler = CSVHandler('test_data.csv', events)
    strategy = SimpleStrategy()
    portfolio = Portfolio(initial_capital=1000000.0)
    broker = Broker()

    print("Starting simulation")

    # our basic loop for simulating the market: we are constantly updating the bars, until our CSV runs out of
    # information. when we receive a new Market Event, we give it over to our selected strategy so it can be handled

    while data_handler.continue_backtest:
        data_handler.update_bars()

        while True:
            try:
                event = events.get(False)
            except queue.Empty:
                break

            print(f"Event caught: {event.type}")

            if event.type == 'MARKET':
                signal = strategy.calculate_signals(event)
                if signal:
                    events.put(signal)

            elif event.type == 'SIGNAL':
                order = portfolio.update_signal(event)
                if order:
                    events.put(order)

            elif event.type == 'ORDER':
                fill = broker.execute_order(event)
                if fill:
                    events.put(fill)

            elif event.type == 'FILL':
                portfolio.update_fill(event)
                print(f"fill received: {fill.symbol} at {fill.fill_cost}$")

    print("Simulation ended")

if __name__ == "__main__":
    main()