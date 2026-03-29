import queue
from src.data.data_manager import prepare_backtest_data
from data.handler import CSVHandler
from strategy.Advanced_Volatility_Strategy import Advanced_Volatility_Strategy
from strategy.Regime_Switch_Strategy import Regime_Switch_Strategy
from portfolio.portfolio import Portfolio
from portfolio.benchmark import Benchmark
from execution.broker import Broker
from src.plotter import Visualizer
from strategy.SMA_Strategy import SMA_Strategy

"""
main: Heart of the System, organizes and executes processes. Implementation of our logic
 to handle events in stages. Gives us necessary data to analyze profitability
"""

def run_backtest(config):
    #preparing data
    data_path = prepare_backtest_data(
        tickers=config['tickers'],
        start=config['start'],
        end=config['end'],
        interval=config['interval']
    )

    #Setup
    events = queue.Queue()
    data_handler = CSVHandler(data_path, events)
    strategy = config['strategy_class']() # Instanziiert die gewählte Klasse

    portfolio = Portfolio(
        stop_loss_pct=config['stop_loss'],
        risk_per_trade_pct=config['risk_per_trade_pct'],
        initial_capital=config['capital']
    )
    benchmark = Benchmark(initial_capital=config['capital'])
    broker = Broker()

    #logic
    print(f"Simuliere Regime-Switch auf {config['tickers']}...")
    while data_handler.continue_backtest:
        data_handler.update_bars()
        while True:
            try:
                event = events.get(False)
            except queue.Empty:
                break

            if event.type == 'MARKET':
                portfolio.update_market(event)
                benchmark.update(event.timestamp, event.symbol, event.end_p)

                curr_pos = portfolio.holdings.get(event.symbol, 0)
                # Stop Loss Check
                if curr_pos > 0:
                    sl_order = portfolio.check_stop_loss(event)
                    if sl_order:
                        events.put(sl_order)
                        continue

                signal = strategy.calculate_signals(event, curr_pos)
                if signal: events.put(signal)

            elif event.type == 'SIGNAL':
                order = portfolio.update_signal(event, broker)
                if order: events.put(order)

            elif event.type == 'ORDER':
                fill = broker.execute_order(event)
                if fill: events.put(fill)

            elif event.type == 'FILL':
                portfolio.update_fill(event)

    #results
    portfolio.liquidate_all_positions(broker)
    stats = portfolio.get_statistics(benchmark.get_curve())
    Visualizer.plot_results(portfolio.equity_curve, stats, benchmark.get_curve())

if __name__ == "__main__":
    #config
    my_config = {
        'tickers': ['SPY'],
        'start': '2020-01-01',
        'end': '2021-01-01',
        'interval': '1d',
        'capital': 1000000.0,
        'stop_loss': 0.2,
        'risk_per_trade_pct': 0.5,
        'strategy_class': Advanced_Volatility_Strategy
    }

    run_backtest(my_config)