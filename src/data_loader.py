import yfinance as yf
import pandas as pd
import os

class DataLoader:
    def __init__(self, ticker, start_date, end_date, data_dir='data'):
        self.ticker = ticker
        self.start_date = start_date
        self.end_date = end_date
        self.data_dir = data_dir
        os.makedirs(self.data_dir, exist_ok=True)

    def fetch_data(self):
        """Fetches historical data from Yahoo Finance."""
        print(f"Fetching data for {self.ticker}...")
        try:
            df = yf.download(self.ticker, start=self.start_date, end=self.end_date, progress=False)
            if df.empty:
                raise ValueError("No data found for the given ticker and date range.")
            
            # Ensure columns are flat if MultiIndex (newer yfinance versions)
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)
            
            # Reset index to make Date a column
            df.reset_index(inplace=True)
            
            save_path = os.path.join(self.data_dir, f"{self.ticker}_{self.start_date}_{self.end_date}.csv")
            df.to_csv(save_path, index=False)
            print(f"Data saved to {save_path}")
            return df
        except Exception as e:
            print(f"Error fetching data: {e}")
            return None

    def load_data(self):
        """Loads data from CSV if exists, else fetches it."""
        file_path = os.path.join(self.data_dir, f"{self.ticker}_{self.start_date}_{self.end_date}.csv")
        if os.path.exists(file_path):
            print(f"Loading data from local file: {file_path}")
            return pd.read_csv(file_path)
        else:
            return self.fetch_data()
