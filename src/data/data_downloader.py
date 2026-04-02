import yfinance as yf
import pandas as pd
import os

def download_advanced_data(tickers, start, end, interval='1h'):
    combined_data = []

    for ticker in tickers:
        print(f"Loading data for {ticker}...")
        df = yf.download(ticker, start=start, end=end, interval=interval)

        if df.empty:
            print(f"Warning: No data for {ticker}")
            continue

        if isinstance(df.columns, pd.MultiIndex):
            if ticker in df.columns.levels[0]:
                df = df[ticker]
            else:
                df.columns = df.columns.get_level_values(0)

        df = df.reset_index()
        df['symbol'] = ticker
        df.rename(columns={
            'Datetime': 'timestamp',
            'Date': 'timestamp',
            'Open': 'open', 'High': 'high', 'Low': 'low', 'Close': 'close', 'Volume': 'volume'
        }, inplace=True)

        columns_to_keep = ['symbol', 'timestamp', 'open', 'high', 'low', 'close', 'volume']
        df = df[columns_to_keep]

        combined_data.append(df)

    final_df = pd.concat(combined_data).sort_values(by='timestamp')

    final_df.to_csv('adv_data.csv', index=False)
    print(f"sucessfully saved: {len(final_df)} data points")