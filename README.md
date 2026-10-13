# Backtesting Engine

This is my backtesting engine for testing different trading strategies, built as a personal project.
Coming from Java, I went with an OOP approach, as this was my first real introduction to Python.

## Features

Since this is an event-driven engine, it works with:

- a central event queue
- a modular design that separates strategies, data handling, the portfolio and execution
- a realistic chain of events (market data, signal, order, fill)
- stop-loss and slippage logic, plus a fixed commission per trade
- a data pipeline from yfinance to analyse historical data
- a buy-and-hold benchmark and a plot of the results with key metrics (return, Sharpe ratio, max drawdown)
- a small Flask REST API and a web dashboard to run backtests from the browser

## Architecture

The event flow works as follows:

```
Market Data -> Strategy -> Signal -> Order -> Broker -> Fill -> Portfolio
```

Every strategy implements one abstract method, `calculate_signals(event, current_pos)`, so strategies can be swapped without touching the rest of the engine.

Included strategies:

- **SMA**: buys when the price is above its short and long moving average, sells when it drops below the short one
- **Advanced Volatility**: moving averages combined with RSI and a volatility filter
- **Regime Switch**: fits a linear regression over the last 30 prices and uses R² to decide the regime. In a sideways market it trades mean reversion (z-score), in a trending market it trades momentum.
- **Simple**: a minimal example strategy

## Structure

```
/src
  /data       - downloads market data (yfinance) and feeds it bar by bar
  /strategy   - strategy logic, abstract base class in base.py
  /portfolio  - cash, positions, stop-loss, statistics, benchmark
  /execution  - broker simulation (commission, slippage)
  event.py    - the event classes
  main.py     - orchestrates the simulation
  plotter.py  - plots the results
api_server.py - Flask REST API (port 5001)
dashboard.html
```

## How to run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements_api.txt

cd src
python main.py          # runs a backtest with the config at the bottom of main.py
```

API and dashboard:

```bash
python api_server.py    # http://localhost:5001
```

Then open `dashboard.html` in the browser. Endpoints: `POST /api/backtest`, `GET /api/results`, `GET /api/stats`, `GET /api/equity-curve`, `GET /health`.

## Known limitations

Things I would do differently or still want to fix:

- Signals and fills use the close of the same bar. Realistically the order would fill at the next bar's open, so results are a bit too optimistic.
- Position sizing is a fixed fraction of equity. Proper risk-based sizing would use the distance to the stop-loss.
- The Sharpe ratio is calculated without a risk-free rate.
- There is no out-of-sample or walk-forward testing yet, so the strategy parameters can be overfitted to the test period.
- No unit tests yet.
