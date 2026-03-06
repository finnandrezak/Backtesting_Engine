import pandas as pd

from src.event import MarketEvent

#CSV Handler to handle the input were currently getting from historic csv datasets

class CSVHandler:
    def __init__(self, csv_file_path, events_queue):
        self.csv_file_path = csv_file_path
        self.events_queue = events_queue

        self.df = pd.read_csv(self.csv_file_path, index_col = 0, parse_dates = True)
        self.df = self.df.sort_index()

        self.continue_backtest = True
        self.counter = 0

    #update method that keeps feeding new events into our event queue until the CSV runs out

    def update_bars(self):
        if self.counter < len(self.df):
            event = MarketEvent()
            self.events_queue.put(event)
            self.counter += 1
        else:
            self.continue_backtest = False

    #Helping method for later analysis to get the latest update

    def get_latest_bar(self):
        return self.df.iloc[self.counter - 1]
