import matplotlib.pyplot as plt
import seaborn as sns
import os
import pandas as pd

class Visualizer:
    def __init__(self, output_dir='outputs'):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        sns.set(style='darkgrid')

    def plot_actual_vs_predicted(self, actual, predicted, model_name, title="Actual vs Predicted Prices"):
        plt.figure(figsize=(12, 6))
        plt.plot(actual, label='Actual Price', color='blue', alpha=0.6)
        plt.plot(predicted, label=f'Predicted Price ({model_name})', color='orange', alpha=0.8)
        plt.title(f"{title} - {model_name}")
        plt.xlabel("Time (Test Set Index)")
        plt.ylabel("Price")
        plt.legend()
        plt.savefig(f"{self.output_dir}/{model_name}_prediction.png")
        plt.close()

    def plot_risk_comparison(self, risk_metrics_dict):
        """
        Comparison of risk metrics across models.
        risk_metrics_dict: { 'ModelName': {'Sharpe': x, 'Var': y ...} }
        """
        df = pd.DataFrame(risk_metrics_dict).T
        
        # Plot Sharpe Ratio
        plt.figure(figsize=(10, 5))
        sns.barplot(x=df.index, y=df['Sharpe Ratio'], hue=df.index, legend=False, palette='viridis')
        plt.title("Sharpe Ratio Comparison")
        plt.ylabel("Sharpe Ratio")
        plt.savefig(f"{self.output_dir}/sharpe_comparison.png")
        plt.close()
        
        # Plot VaR
        plt.figure(figsize=(10, 5))
        sns.barplot(x=df.index, y=df['VaR (95%)'], hue=df.index, legend=False, palette='magma')
        plt.title("Value at Risk (95%) Comparison")
        plt.ylabel("VaR")
        plt.savefig(f"{self.output_dir}/var_comparison.png")
        plt.close()

    def plot_model_performance(self, perf_metrics_dict):
        """
        Comparison of evaluation metrics (RMSE, MAPE).
        perf_metrics_dict: { 'ModelName': {'RMSE': x, 'MAPE': y ...} }
        """
        df = pd.DataFrame(perf_metrics_dict).T
        
        # Plot RMSE
        plt.figure(figsize=(10, 5))
        sns.barplot(x=df.index, y=df['RMSE'], hue=df.index, legend=False, palette='Blues_d')
        plt.title("RMSE Comparison (Lower is Better)")
        plt.ylabel("RMSE")
        plt.savefig(f"{self.output_dir}/rmse_comparison.png")
        plt.close()
