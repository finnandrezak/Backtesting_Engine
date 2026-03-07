This my current raw structure for a Backtesting engine in order to test different trading strategies as a personal project.
Coming from java and not having that much experience, i went with a rather simple OOP approach, as this is my first real introduction
to Python. As I progress in programming, im planning to upgrade this raw framework more and more from here on out, with the endgoal being
to simulate a real market with real time data, real spreads, etc. making the results as realistic as they can be.

Features:
Since this is an event driven Engine, im working with the following features:
a central event queue
a modular desgin separating strategies, data handling, the portfolio etc.
a realistic chain of events

Architecture: 
OOP based, the described event flow works as follows:
Market Data -> Strategy -> Signal -> Order -> Broker -> Fill -> Portfolio

Structure:
/src
  /data      - CSV handler for market Data
  /strategy  - strategy logic
  /portfolio - depot and cash management
  /execution - broker simulation
  event.py   - different event classes
main.py      - orchestrates the simulation

Roadmap:
Implementing a real trading strategy(MA crossover)
Visualization of Profit/Loss
Larger datasets, at some point implementing realtime Data
replacingt dummy values with realistic scenarios


