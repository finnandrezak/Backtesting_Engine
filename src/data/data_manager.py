import yfinance as yf
import pandas as pd
import os

"""
Data Manager: orchestrates download and processing of data
returns path to the created csv
"""

def prepare_backtest_data(tickers, start, end, interval='1h'):

    combined_data = []
    print(f"--- Starte Daten-Vorbereitung für: {tickers} ---")

    for ticker in tickers:
        df = yf.download(ticker, start=start, end=end, interval=interval)
        if df.empty:
            print(f"Warning: Keine Daten für {ticker}")
            continue

        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        df = df.reset_index()
        df['symbol'] = ticker

        rename_map = {
            'Datetime': 'timestamp', 'Date': 'timestamp',
            'Open': 'open', 'High': 'high', 'Low': 'low',
            'Close': 'close', 'Volume': 'volume'
        }
        df.rename(columns=rename_map, inplace=True)

        cols = ['symbol', 'timestamp', 'open', 'high', 'low', 'close', 'volume']
        df = df[[c for c in cols if c in df.columns]]
        combined_data.append(df)

    if not combined_data:
        return None

    final_df = pd.concat(combined_data).sort_values(by='timestamp')
    output_path = 'adv_data.csv'
    final_df.to_csv(output_path, index=False)

    print(f"--- Daten bereit: {len(final_df)} Zeilen in {output_path} ---")
    return output_path