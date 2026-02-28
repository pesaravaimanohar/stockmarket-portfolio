import pandas as pd
import numpy as np

class FeatureEngineer:
    def __init__(self, df):
        self.df = df.copy()
        # Ensure Date is datetime and set as index if needed for rolling ops, 
        # but usually pandas rolling works on columns.
        if 'Date' in self.df.columns:
            self.df['Date'] = pd.to_datetime(self.df['Date'])
            self.df.sort_values('Date', inplace=True)

    def compute_rsi(self, window=14, col='Close'):
        """Computes Relative Strength Index (RSI)."""
        delta = self.df[col].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
        rs = gain / loss
        self.df['RSI'] = 100 - (100 / (1 + rs))
        return self.df

    def compute_macd(self, slow=26, fast=12, signal=9, col='Close'):
        """Computes Moving Average Convergence Divergence (MACD)."""
        exp1 = self.df[col].ewm(span=fast, adjust=False).mean()
        exp2 = self.df[col].ewm(span=slow, adjust=False).mean()
        self.df['MACD'] = exp1 - exp2
        self.df['Signal_Line'] = self.df['MACD'].ewm(span=signal, adjust=False).mean()
        return self.df

    def compute_moving_averages(self, windows=[20, 50, 200], col='Close'):
        """Computes Simple Moving Averages."""
        for w in windows:
            self.df[f'MA_{w}'] = self.df[col].rolling(window=w).mean()
        return self.df

    def compute_volatility(self, window=20, col='Close'):
        """Computes rolling volatility (standard deviation)."""
        # Volatility is usually std dev of returns, or just std dev of price.
        # Requirement says: "Volatility (standard deviation of returns)" in the Risk section,
        # but for feature engineering, price volatility is also useful. 
        # I'll add daily returns and their rolling std dev.
        self.df['Daily_Return'] = self.df[col].pct_change()
        self.df['Volatility'] = self.df['Daily_Return'].rolling(window=window).std()
        return self.df

    def create_lag_features(self, lags=[1, 2, 3, 5], col='Close'):
        """Creates lag features for time series forecasting."""
        for lag in lags:
            self.df[f'Lag_{lag}'] = self.df[col].shift(lag)
        return self.df

    def prepare_data(self):
        """Runs all feature generation methods and cleans NaN values."""
        self.compute_rsi()
        self.compute_macd()
        self.compute_moving_averages()
        self.compute_volatility()
        self.create_lag_features()
        
        # Drop rows with NaN created by windowing/shifting
        self.df.dropna(inplace=True)
        return self.df
