import argparse
import pandas as pd
import numpy as np
from src.data_loader import DataLoader
from src.feature_engineering import FeatureEngineer
from src.models import ModelTrainer
from src.risk_analysis import RiskAnalyzer
from src.evaluation import evaluate_predictions
from src.visualization import Visualizer

def main(ticker='AAPL', start_date='2020-01-01', end_date='2023-01-01'):
    print("====================================")
    print("Risk-Aware Stock Price Forecasting")
    print("====================================")

    # 1. Data Ingestion
    loader = DataLoader(ticker, start_date, end_date)
    df = loader.load_data()
    if df is None:
        return

    # 2. Feature Engineering
    print("\n[Step 2] Feature Engineering...")
    fe = FeatureEngineer(df)
    df_features = fe.prepare_data()
    print(f"Features created. New shape: {df_features.shape}")
    print(f"Columns: {df_features.columns.tolist()}")

    # 3. Model Training
    print("\n[Step 3] Model Training...")
    # Using 'Close' as target. Note: In a real scenario, we'd shift Target to be t+1. 
    # Current setup predicts Close(t) using Features(t) which includes Lags of (t).
    trainer = ModelTrainer(df_features, target_col='Close')
    X_train, X_test, y_train, y_test = trainer.split_data()

    models_to_run = ['LinearRegression', 'RandomForest', 'XGBoost', 'LSTM', 'BiLSTM']
    trained_models = {}
    
    trainer.train_linear_regression()
    trainer.train_random_forest()
    trainer.train_xgboost()
    trainer.train_lstm()
    trainer.train_bi_lstm()

    # 4. Evaluation & Risk Analysis
    print("\n[Step 4 & 5] Evaluation & Risk Analysis...")
    visualizer = Visualizer()
    results = {}
    risk_results = {}

    for name in models_to_run:
        print(f"\nEvaluating {name}...")
        try:
            # Get predictions
            preds = trainer.predict(name)
            # Get actuals (aligned with preds)
            actuals = trainer.get_actual_values(name)
            
            # Ensure lengths match (sometimes LSTM drops more data due to batches/seq)
            min_len = min(len(preds), len(actuals))
            preds = preds[:min_len]
            actuals = actuals[:min_len]

            # Evaluate Accuracy
            metrics = evaluate_predictions(actuals, preds)
            results[name] = metrics
            print(f"  RMSE: {metrics['RMSE']:.4f}")
            print(f"  MAPE: {metrics['MAPE']:.2f}%")

            # Risk Analysis
            risk_analyzer = RiskAnalyzer(actuals, preds)
            r_metrics = risk_analyzer.get_risk_metrics()
            score = risk_analyzer.risk_aware_decision_score(0, r_metrics) # Placeholder for return prediction
            r_metrics['Decision Score'] = score
            risk_results[name] = r_metrics
            print(f"  VaR (95%): {r_metrics['VaR (95%)']:.4f}")
            print(f"  Sharpe Ratio: {r_metrics['Sharpe Ratio']:.4f}")

            # Visualization
            visualizer.plot_actual_vs_predicted(actuals, preds, name)
            
        except Exception as e:
            print(f"Error evaluating {name}: {e}")

    # Comparative Plots
    visualizer.plot_model_performance(results)
    visualizer.plot_risk_comparison(risk_results)

    print("\n====================================")
    print("Final Analysis Complete.")
    print("Check 'outputs/' folder for graphs and 'data/' for datasets.")
    print("====================================")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--ticker', type=str, default='AAPL', help='Stock Ticker Symbol')
    parser.add_argument('--start', type=str, default='2020-01-01', help='Start Date (YYYY-MM-DD)')
    parser.add_argument('--end', type=str, default='2023-01-01', help='End Date (YYYY-MM-DD)')
    args = parser.parse_args()
    
    main(args.ticker, args.start, args.end)
