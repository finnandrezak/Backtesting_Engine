import queue
from data.handler import CSVHandler
from strategy.SimpleStrategy import SimpleStrategy

#this is were we actually start our simulation of the market. first we start an event queue aswell as a new data handler with our CSV as the input

def main():
    events = queue.Queue()
    data_handler = CSVHandler('test_data.csv', events)
    strategy = SimpleStrategy()

    print("Starting simulation")

    # our basic loop for simulating the market: we are constantly updating the bars, until our CSV runs out of
    # information. when we receive a new Market Event, we give it over to our selected strategy so it can be handled

    while data_handler.continue_backtest:
        data_handler.update_bars()

        try:
            event = events.get(False)
            print(f"Event caught: {event.type}")

            if event.type == 'MARKET':
                signal = strategy.calculate_signals(event)
                if signal:
                    print(f"Signal generated: {signal.signal_type} for: {signal.symbol}")
        except:
            pass

    print("Simulation ended ended")
if __name__ == '__main__':
  main()