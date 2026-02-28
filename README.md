# Risk-Aware Stock Price Forecasting Using Machine Learning and Deep Learning Techniques

## Project Overview
This project is an advanced stock forecasting system designed for an MCA final year project. It goes beyond simple price prediction by integrating **Risk Management** metrics.

### Key Objectives
1. **Predict** stock prices using Classical ML (Linear Regression, Random Forest, XGBoost) and Deep Learning (LSTM, Bi-LSTM).
2. **Quantify Risk** using Volatility, Value at Risk (VaR), Max Drawdown, and Sharpe Ratio.
3. **Decision Support** via a Risk-Aware Decision Score.

## Project Structure
```
stock_project/
├── data/                   # Stores downloaded stock data
├── outputs/                # Generated plots and visualizations
├── src/
│   ├── data_loader.py      # Fetches proprietary data from Yahoo Finance
│   ├── feature_engineering.py # Technical Indicators (RSI, MACD, etc.)
│   ├── models.py           # ML & DL Model Definitions
│   ├── risk_analysis.py    # VaR, Drawdown, Sharpe Calculations
│   ├── evaluation.py       # RMSE, MAPE, Directional Accuracy
│   └── visualization.py    # Plotting utilities
├── main.py                 # Main execution script
└── requirements.txt        # Python dependencies
```

## Setup Instructions

### 1. Prerequisites
- Python 3.8+
- Internet connection (to fetch stock data)

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Project
You can run the main script with default settings (Apple stock, 2020-2023):
```bash
python main.py
```

Or specify a custom ticker and date range:
```bash
python main.py --ticker GOOGL --start 2018-01-01 --end 2024-01-01
```

## Features Implemented

### Technical Indicators
- **RSI (Relative Strength Index)**: Momentum indicator.
- **MACD**: Trend-following momentum indicator.
- **Moving Averages (20, 50, 200)**: Trend smoothing.
- **Volatility**: Rolling standard deviation.

### Models
1. **Linear Regression**: Baseline model.
2. **Random Forest**: Ensemble learning for non-linear relationships.
3. **XGBoost**: Gradient boosting for high performance.
4. **LSTM (Long Short-Term Memory)**: Recurrent Neural Network for time-series.
5. **Bi-LSTM**: Bidirectional LSTM for capturing future/past context in training.

### Risk Metrics
- **Value at Risk (VaR)**: estimating the maximum potential loss.
- **Sharpe Ratio**: Risk-adjusted return.
- **Maximum Drawdown**: Worst peak-to-trough decline.

## Results
Check the `outputs/` folder after running the script. It will contain:
- `LSTM_prediction.png`
- `XGBoost_prediction.png`
- `rmse_comparison.png`
- `sharpe_comparison.png`

## Authors
- [Your Name/ID]
- JNTUA MCA Department
