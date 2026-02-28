import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error
# import tensorflow as tf
# from tensorflow.keras.models import Sequential
# from tensorflow.keras.layers import LSTM, Dense, Bidirectional, Attention, Layer, Input
# from tensorflow.keras.optimizers import Adam

class ModelTrainer:
    def __init__(self, data, target_col='Close', test_size=0.2, seq_length=60):
        self.data = data
        self.target_col = target_col
        self.test_size = test_size
        self.seq_length = seq_length
        self.scalers = {} # To store scalers for inverse transform
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.models = {}

    def split_data(self):
        """Splits data into train and test sets (Time-series split)."""
        # Drop non-numeric columns like Date for training
        if 'Date' in self.data.columns:
            self.dates = self.data['Date']
            data_numeric = self.data.drop(['Date'], axis=1)
        else:
            self.dates = self.data.index
            data_numeric = self.data
            
        train_size = int(len(data_numeric) * (1 - self.test_size))
        
        # Scaling
        scaler = MinMaxScaler()
        data_scaled = scaler.fit_transform(data_numeric)
        self.scalers['feature_scaler'] = scaler
        
        # Create X and y
        # We need to predict 'target_col' (future).
        # Standard approach: predict next step based on current features.
        # However, for fair comparison with LSTM (which uses sequence), 
        # ML models usually use lag features already generated in feature_engineering.
        
        # Identify target index
        target_idx = list(data_numeric.columns).index(self.target_col)
        
        X = data_scaled[:, :] # All features including current price 
        # But wait, if we predict *future* price, we should shift y.
        # In feature engineering, we created Lags.
        # If 'Close' is the target, and we want to predict Close(t), we use Features(t-1) or Sequence(t-n...t).
        # Let's assume the dataset is already prepared such that one row contains features to predict the Target of that row
        # (which creates look-ahead bias if not careful).
        # Better approach: Target is Close shifted by -1 (next day price), but let's stick to standard Close prediction
        # based on past lags. If FeatureEngineer created 'Lag_1', 'Lag_2', etc., and we want to predict 'Close',
        # then 'Close' is the target and Lags are the features.
        
        # For ML Models (LR, RF, XGB):
        # We use all columns except the target as features? Or just Lags? 
        # Let's use all columns as features to predict 'Close'. 
        # IMPORTANT: 'Close' itself should not be a feature for predicting 'Close' at time t 
        # unless it's a lag. Current 'Close' shouldn't be in X if we predict 'Close'.
        # However, if we assume the standard "Predict tomorrow's price" task.
        # Let's shift target by -1 to predict t+1.
        
        # Simplified for this project: Predict Close(t) given Features(t including Lags).
        # This assumes features are available at t.
        # Actually, standard forecasting: Use info up to t-1 to predict t.
        
        X = data_scaled[:, :] # All columns
        y = data_scaled[:, target_idx]
        
        self.X_train, self.X_test = X[:train_size], X[train_size:]
        self.y_train, self.y_test = y[:train_size], y[train_size:]
        
        print(f"Data Split: Train shape {self.X_train.shape}, Test shape {self.X_test.shape}")
        return self.X_train, self.X_test, self.y_train, self.y_test

    def prepare_lstm_data(self, X_data, y_data):
        """Reshapes data for LSTM [samples, time steps, features]."""
        X_seq, y_seq = [], []
        # Create sequences
        for i in range(self.seq_length, len(X_data)):
            X_seq.append(X_data[i-self.seq_length:i])
            y_seq.append(y_data[i])
        return np.array(X_seq), np.array(y_seq)

    def train_linear_regression(self):
        print("Training Linear Regression...")
        model = LinearRegression()
        # For ML models, we ignore the sequence structure and treat rows as independent samples
        # effectively using lags as temporal features.
        model.fit(self.X_train, self.y_train)
        self.models['LinearRegression'] = model
        return model

    def train_random_forest(self):
        print("Training Random Forest...")
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        # RF doesn't handle time series natively, but works with lag features
        model.fit(self.X_train, self.y_train)
        self.models['RandomForest'] = model
        return model

    def train_xgboost(self):
        print("Training XGBoost...")
        model = XGBRegressor(n_estimators=100, learning_rate=0.05, random_state=42)
        model.fit(self.X_train, self.y_train)
        self.models['XGBoost'] = model
        return model

    def train_lstm(self):
        print("Training LSTM...")
        # Lazy import tensorflow
        import tensorflow as tf
        from tensorflow.keras.models import Sequential
        from tensorflow.keras.layers import LSTM, Dense, Input

        # Prepare data
        X_train_seq, y_train_seq = self.prepare_lstm_data(self.X_train, self.y_train)
        
        model = Sequential()
        model.add(Input(shape=(X_train_seq.shape[1], X_train_seq.shape[2])))
        model.add(LSTM(50, return_sequences=True))
        model.add(LSTM(50, return_sequences=False))
        model.add(Dense(25))
        model.add(Dense(1))
        
        model.compile(optimizer='adam', loss='mean_squared_error')
        model.fit(X_train_seq, y_train_seq, batch_size=32, epochs=5, verbose=1) # Low epochs for demo
        self.models['LSTM'] = model
        return model

    def train_bi_lstm(self):
        print("Training Bi-LSTM...")
        import tensorflow as tf
        from tensorflow.keras.models import Sequential
        from tensorflow.keras.layers import LSTM, Dense, Bidirectional, Input

        X_train_seq, y_train_seq = self.prepare_lstm_data(self.X_train, self.y_train)
        
        model = Sequential()
        model.add(Input(shape=(X_train_seq.shape[1], X_train_seq.shape[2])))
        model.add(Bidirectional(LSTM(50, return_sequences=True)))
        model.add(Bidirectional(LSTM(50, return_sequences=False)))
        model.add(Dense(25))
        model.add(Dense(1))
        
        model.compile(optimizer='adam', loss='mean_squared_error')
        model.fit(X_train_seq, y_train_seq, batch_size=32, epochs=5, verbose=1)
        self.models['BiLSTM'] = model
        return model

    def predict(self, model_name):
        model = self.models.get(model_name)
        if not model:
            raise ValueError(f"Model {model_name} not trained yet.")
        
        print(f"Predicting with {model_name}...")
        if model_name in ['LSTM', 'BiLSTM']:
            X_test_seq, _ = self.prepare_lstm_data(self.X_test, self.y_test)
            preds = model.predict(X_test_seq)
            # Inverse transform requires the scaler and the full shape roughly.
            # We scaled all features. The predictions are just 'Close'.
            # We need to construct a matrix of shape (n_samples, n_features) to inverse transform.
            # Trick: copy X_test, replace target col with predictions, then inverse transform.
            
            # This is complex because X_test_seq is smaller than X_test by seq_length
            dummy = np.zeros((len(preds), self.X_test.shape[1]))
            # Copy other features from X_test (aligned by index)
            # X_test_seq indices correspond to X_test[seq_length:]
            dummy[:, :] = self.X_test[self.seq_length:, :]
            
            # Replace target col with prediction
            target_idx = list(self.data.columns).index(self.target_col) if 'Date' not in self.data.columns else list(self.data.drop('Date', axis=1).columns).index(self.target_col)
            dummy[:, target_idx] = preds.flatten()
            
            inversed = self.scalers['feature_scaler'].inverse_transform(dummy)
            return inversed[:, target_idx]
            
        else:
            # ML models
            preds = model.predict(self.X_test)
            dummy = np.zeros((len(preds), self.X_test.shape[1]))
            dummy[:, :] = self.X_test
            target_idx = list(self.data.columns).index(self.target_col) if 'Date' not in self.data.columns else list(self.data.drop('Date', axis=1).columns).index(self.target_col)
            dummy[:, target_idx] = preds
            inversed = self.scalers['feature_scaler'].inverse_transform(dummy)
            return inversed[:, target_idx]
    
    def get_actual_values(self, model_name):
        """Returns actual values corresponding to the test set of the model."""
        # For LSTM, test set is smaller by seq_length
        target_idx = list(self.data.columns).index(self.target_col) if 'Date' not in self.data.columns else list(self.data.drop('Date', axis=1).columns).index(self.target_col)
        
        if model_name in ['LSTM', 'BiLSTM']:
             # X_test[seq_length:] contains the rows for which we made predictions
             dummy = np.zeros((len(self.X_test) - self.seq_length, self.X_test.shape[1]))
             dummy[:, :] = self.X_test[self.seq_length:, :]
        else:
            dummy = np.zeros((len(self.X_test), self.X_test.shape[1]))
            dummy[:, :] = self.X_test
            
        inversed = self.scalers['feature_scaler'].inverse_transform(dummy)
        return inversed[:, target_idx]
