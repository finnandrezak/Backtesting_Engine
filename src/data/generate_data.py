import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# --- Configuration ---
n_steps = 500  # 500 minutes * 2 symbols = 1000 rows
start_time = datetime(2026, 3, 10, 9, 30)
symbols = ['AAPL', 'TSLA']
start_prices = {'AAPL': 150.0, 'TSLA': 650.0}
# Volatility: how much the price swings per minute
volatility = {'AAPL': 0.0012, 'TSLA': 0.0028}

rows = []

for symbol in symbols:
    current_price = start_prices[symbol]
    for i in range(n_steps):
        ts = start_time + timedelta(minutes=i)

        # Random Walk with a tiny upward bias (0.0001)
        change = np.random.normal(0.0001, volatility[symbol])
        o = current_price
        c = o * (1 + change)

        # Generate High/Low slightly outside of Open/Close
        h = max(o, c) + (abs(np.random.normal(0, 0.1)))
        l = min(o, c) - (abs(np.random.normal(0, 0.1)))
        v = np.random.randint(5000, 50000)

        rows.append([symbol, ts.strftime('%Y-%m-%d %H:%M:%S'),
                     round(o, 2), round(h, 2), round(l, 2), round(c, 2), v])

        # Next candle starts where the previous one closed
        current_price = c

# Create DataFrame using YOUR structure
df = pd.DataFrame(rows, columns=['symbol', 'timestamp', 'open', 'high', 'low', 'close', 'volume'])

# CRITICAL: Sort by timestamp so the symbols are interleaved (Market-like feed)
df['timestamp'] = pd.to_datetime(df['timestamp'])
df = df.sort_values('timestamp').reset_index(drop=True)

# Save to CSV
df.to_csv('data.csv', index=False)
print(f"Successfully generated 'data.csv' with {len(df)} rows.")
print(df.head(5))