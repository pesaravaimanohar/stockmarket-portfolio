# Technical Explanation for MCA Viva
## Project: Risk-Aware Stock Price Forecasting

### 1. Abstract
This project focuses on predicting stock market trends while simultaneously assessing the associated financial risks. Unlike traditional forecasting systems that only minimize error (RMSE), this system optimizes for **risk-adjusted returns**.

### 2. Motivation
Stock markets are volatile. A model might predict high returns but with extreme risk (high variance). For an investor, knowing the "potential acceptable loss" (VaR) is as important as the profit.

### 3. Architecture
The system follows a standard MLOps pipeline:
1.  **ETL**: Extract data from Yahoo Finance API.
2.  **Feature Engineering**: We transform raw prices (Open, Close) into meaningful signals:
    *   **RSI**: Identifies overbought/oversold conditions.
    *   **MACD**: Captures trend momentum.
    *   **Lags**: Essential for time-series regression (using yesterday's value to predict today's).
3.  **Modeling**:
    *   **Machine Learning (RF, XGBoost)**: Good at capturing non-linear interactions between indicators.
    *   **Deep Learning (LSTM)**: Specifically designed for sequence data, maintaining an internal "state" to remember long-term trends.
    *   **Bi-LSTM**: Processes data in both forward and backward directions to capture context better.

### 4. Key Algorithms Explained
*   **LSTM (Long Short-Term Memory)**: Solves the "vanishing gradient" problem of standard RNNs. It uses a "forget gate" to decide what information to keep from previous time steps.
*   **VaR (Value at Risk)**: We calculate the 95% VaR, meaning "We are 95% confident that the loss will not exceed X% in a day."
*   **Sharpe Ratio**: Measures "Return per unit of Risk." Formula: $(R_p - R_f) / \sigma_p$.

### 5. Results & Challenges
*   **Stationarity**: Stock data is non-stationary (mean and variance change over time). We addressed this by using "Returns" (percentage change) for volatility calculation and scaling inputs using MinMax Scaler.
*   **Overfitting**: Deep learning models tend to overfit on noise. We used a simple architecture and could add Dropout layers for improvement.

### 6. Future Scope
*   Integration with Sentiment Analysis (News/Twitter).
*   Reinforcement Learning (RL) agent for automated trading execution.
