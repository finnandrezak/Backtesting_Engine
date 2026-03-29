This is my Backtesting engine in order to test different trading strategies as a personal project.
Coming from java, i went with an OOP approach, as this is my first real introduction to Python. 

Features:
Since this is an event driven Engine, im working with the following features:
a central event queue
a modular desgin separating strategies, data handling, the portfolio etc.
a realistic chain of events
stop loss, order slip  logic
data pipeline from Yfinance to analyze historical data
plot for results including benchmark and key data

Architecture: 
OOP based, the described event flow works as follows:
Market Data -> Strategy -> Signal -> Order -> Broker -> Fill -> Portfolio

Structure:
/src
  /data      - CSV generator and handler for market Data
  /strategy  - strategy logic
  /portfolio - depot and cash management
  /execution - broker simulation
  event.py   - different event classes
main.py      - orchestrates the simulation
plotter.py   - plots results

Roadmap:
Strategy optimization
Bug fixing
Advanced Analytics
CSV -> Parquet


