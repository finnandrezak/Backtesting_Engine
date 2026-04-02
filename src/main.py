import queue
from data.data_manager import prepare_backtest_data
from data.handler import CSVHandler
from strategy.Advanced_Volatility_Strategy import Advanced_Volatility_Strategy
from strategy.Regime_Switch_Strategy import Regime_Switch_Strategy
from strategy.SMA_Strategy import SMA_Strategy
from portfolio.portfolio import Portfolio
from portfolio.benchmark import Benchmark
from execution.broker import Broker
from plotter import Visualizer

def run_backtest(config, show_plot=False):
    data_path = prepare_backtest_data(
        tickers=config['tickers'],
        start=config['start'],
        end=config['end'],
        interval=config['interval']
    )

    events = queue.Queue()
    data_handler = CSVHandler(data_path, events)
    strategy = config['strategy_class']()

    portfolio = Portfolio(
        stop_loss_pct=config['stop_loss'],
        risk_per_trade_pct=config['risk_per_trade_pct'],
        initial_capital=config['capital']
    )
    benchmark = Benchmark(initial_capital=config['capital'])
    broker = Broker()

    print(f"Backtesting on {config['tickers']}...")
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

    portfolio.liquidate_all_positions(broker)
    stats = portfolio.get_statistics(benchmark.get_curve())
    
    if show_plot:
        Visualizer.plot_results(portfolio.equity_curve, stats, benchmark.get_curve())
    
    print("\n" + "="*50)
    print("BACKTEST RESULTS")
    print("="*50)
    print(f"Initial Capital: ${config['capital']:,.2f}")
    print(f"Final Equity: ${stats['final']:,.2f}")
    print(f"Return: {stats['return_pct']:.2f}%")
    print(f"Sharpe Ratio: {stats['sharpe_ratio']:.2f}")
    print(f"Max Drawdown: {stats['max_drawdown']:.2f}%")
    print(f"Trades: {len(portfolio.trades)}")
    print("="*50 + "\n")
    
    return portfolio, stats, benchmark

if __name__ == "__main__":
    config = {
        'tickers': ['SPY'],
        'start': '2020-01-01',
        'end': '2021-01-01',
        'interval': '1d',
        'capital': 1000000.0,
        'stop_loss': 0.2,
        'risk_per_trade_pct': 0.5,
        'strategy_class': Regime_Switch_Strategy
    }
    run_backtest(config, show_plot=True)
