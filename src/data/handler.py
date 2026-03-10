import pandas as pd

from src.event import MarketEvent

#CSV Handler to handle the input were currently getting from historic csv datasets

class CSVHandler:
    def __init__(self, csv_file_path, events_queue):
        self.csv_file_path = csv_file_path
        self.events_queue = events_queue

        self.df = pd.read_csv(self.csv_file_path)

        if 'timestamp' in self.df.columns:
            self.df['timestamp'] = pd.to_datetime(self.df['timestamp'])
            self.df = self.df.sort_values('timestamp')

        self.continue_backtest = True
        self.counter = 0
        print(f"Erfolgreich geladen: {len(self.df)} Zeilen.")

    #update method that keeps feeding new events into our event queue until the CSV runs out

    def update_bars(self):

        if self.counter < len(self.df):
            row = self.df.iloc[self.counter]

            symbol = row['symbol']
            timestamp = row['timestamp']
            open_p = float(row['open'])
            high_p = float(row['high'])
            low_p = float(row['low'])
            end_p = float(row['close'])
            volume = int(row['volume'])

            event = MarketEvent(
                symbol=symbol,
                timestamp=timestamp,
                open_p=open_p,
                high_p=high_p,
                low_p=low_p,
                end_p=end_p,
                volume=volume
            )

            self.events_queue.put(event)
            self.counter += 1

            print(f"DataHandler: {symbol} @ {end_p} ({timestamp}) gesendet.")
        else:
            self.continue_backtest = False
    #Helping method for later analysis to get the latest update

    def get_latest_bar(self):
        return self.df.iloc[self.counter - 1]
