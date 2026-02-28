import numpy as np
import pandas as pd

class RiskAnalyzer:
    def __init__(self, actual_prices, predicted_prices):
        self.actual = np.array(actual_prices)
        self.predicted = np.array(predicted_prices)
        
    def calculate_volatility(self, prices=None):
        """Std dev of returns."""
        if prices is None:
            prices = self.predicted
        returns = np.diff(prices) / prices[:-1]
        return np.std(returns)

    def calculate_max_drawdown(self, prices=None):
        """Maximum observed loss from a peak to a trough."""
        if prices is None:
            prices = self.predicted
        peak = prices[0]
        max_drawdown = 0
        for price in prices:
            if price > peak:
                peak = price
            dd = (peak - price) / peak
            if dd > max_drawdown:
                max_drawdown = dd
        return max_drawdown

    def calculate_var(self, prices=None, confidence_level=0.95):
        """Value at Risk using Historical Simulation method on returns."""
        if prices is None:
            prices = self.predicted
        returns = np.diff(prices) / prices[:-1]
        if len(returns) == 0:
            return 0.0
        # Sort returns
        sorted_returns = np.sort(returns)
        # Index for Var
        index = int((1 - confidence_level) * len(sorted_returns))
        return abs(sorted_returns[index]) # Return as positive percentage

    def calculate_sharpe_ratio(self, prices=None, risk_free_rate=0.0):
        """Annualized Sharpe Ratio (assuming daily data, 252 trading days)."""
        if prices is None:
            prices = self.predicted
        returns = np.diff(prices) / prices[:-1]
        mean_return = np.mean(returns)
        std_return = np.std(returns)
        if std_return == 0:
            return 0.0
        annualized_return = mean_return * 252
        annualized_std = std_return * np.sqrt(252)
        return (annualized_return - risk_free_rate) / annualized_std

    def get_risk_metrics(self):
        """Returns a dict of all risk metrics."""
        return {
            "Volatility": self.calculate_volatility(),
            "Max Drawdown": self.calculate_max_drawdown(),
            "VaR (95%)": self.calculate_var(),
            "Sharpe Ratio": self.calculate_sharpe_ratio()
        }

    def risk_aware_decision_score(self, predicted_return, risk_metrics):
        """
        Custom score: (Predicted Return / Risk) 
        Simple weights: 0.6 * Return_Score - 0.4 * Risk_Score
        This is a heuristic.
        """
        # Simplify: Sharpe Ratio is essentially this.
        # Let's create a score 0-100.
        # High Sharpe is good. Low Max Drawdown is good.
        
        # Example logic:
        # Score = (Sharpe * 10) + (1 - Drawdown)*50 - (VaR * 100)
        sharpe = risk_metrics.get("Sharpe Ratio", 0)
        dd = risk_metrics.get("Max Drawdown", 0)
        var = risk_metrics.get("VaR (95%)", 0)
        
        score = (sharpe * 10) + ((1 - dd) * 50) - (var * 100)
        return max(0, min(100, score)) # Clip between 0 and 100
