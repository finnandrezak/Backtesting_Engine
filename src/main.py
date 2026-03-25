import queue
import matplotlib.pyplot as plt

from portfolio.benchmark import Benchmark
from src.plotter import Visualizer
from data.handler import CSVHandler
from execution.broker import Broker
from strategy.SMA_Strategy import SMA_Strategy
from strategy.SimpleStrategy import SimpleStrategy
from portfolio.portfolio import Portfolio


"""
main: Heart of the System, organizes and executes processes. Implementation of our logic
 to handle events in stages. Gives us necessary data to analyze profitability

"""
def main():
    events = queue.Queue()
    data_handler = CSVHandler('adv_data.csv', events)
    strategy = SMA_Strategy()
    portfolio = Portfolio(strategy.stop_loss_pct, initial_capital=1000000.0)
    benchmark = Benchmark(initial_capital=1000000.0)
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
                portfolio.update_market(event)
                benchmark.update(event.timestamp, event.symbol, event.end_p)
                sl_order = portfolio.check_stop_loss(event)

                if sl_order:
                    events.put(sl_order)
                    continue

                signal = strategy.calculate_signals(event)
                if signal:
                    events.put(signal)

            elif event.type == 'SIGNAL':
                order = portfolio.update_signal(event, broker)
                if order:
                    events.put(order)

            elif event.type == 'ORDER':
                fill = broker.execute_order(event)
                if fill:
                    events.put(fill)

            elif event.type == 'FILL':
                portfolio.update_fill(event)
                print(f"fill received: {event.symbol} at {event.fill_cost}$")

    print("Market data finished. Closing all open positions...")
    portfolio.liquidate_all_positions(broker)

    print("Simulation ended")
    print(f"total value: {portfolio.get_equity()} $")

    #visual presentation of equity curve and statistics with matplot lib
    stats = portfolio.get_statistics(benchmark.get_curve())
    Visualizer.plot_results(portfolio.equity_curve, stats, benchmark.get_curve())

if __name__ == "__main__":
    main()