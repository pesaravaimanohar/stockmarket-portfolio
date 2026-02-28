import sys
import os
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import pandas as pd
import numpy as np
import traceback

# Add parent directory to path to allow importing from src
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.data_loader import DataLoader
from src.feature_engineering import FeatureEngineer
from src.models import ModelTrainer
from src.risk_analysis import RiskAnalyzer
from src.evaluation import evaluate_predictions

app = FastAPI(title="AntigravityStocks API", version="1.0.0")

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class StockRequest(BaseModel):
    ticker: str
    start_date: str
    end_date: str

class ChartPoint(BaseModel):
    date: str
    actual: Optional[float]
    predicted: Optional[float]

class Metrics(BaseModel):
    RMSE: float
    MAPE: float
    VaR_95: float
    Sharpe_Ratio: float
    Decision_Score: float
    Volatility: str

class PredictionResponse(BaseModel):
    ticker: str
    model: str
    metrics: Metrics
    chart_data: List[ChartPoint]
    current_price: float
    predicted_high: float

@app.post("/predict", response_model=PredictionResponse)
async def predict(request: StockRequest):
    try:
        print(f"Received request: {request}")
        
        # 1. Load Data
        loader = DataLoader(request.ticker, request.start_date, request.end_date)
        df = loader.load_data()
        
        if df is None or df.empty:
            raise HTTPException(status_code=404, detail="No data found for ticker")

        # 2. Feature Engineering
        fe = FeatureEngineer(df)
        df_features = fe.prepare_data()

        # 3. Model Training (Fastest Model for API - XGBoost)
        # Note: In a real app, successful models are saved/loaded. 
        # Here we train on the fly as per original script design.
        trainer = ModelTrainer(df_features, target_col='Close')
        X_train, X_test, y_train, y_test = trainer.split_data()
        
        model_name = 'XGBoost'
        trainer.train_xgboost()
        
        # 4. Predictions & Evaluation
        preds = trainer.predict(model_name)
        actuals = trainer.get_actual_values(model_name)
        
        # Alignment
        min_len = min(len(preds), len(actuals))
        preds = preds[:min_len]
        actuals = actuals[:min_len]
        
        # Get dates for the test set
        # The test set is the last 20% by default in ModelTrainer (check implementation)
        # We need to map these back to dates. 
        # Assuming simple time-series split implies last N records.
        # Prepare dates
        if not pd.api.types.is_datetime64_any_dtype(df_features.index):
             # Try to convert if it's not already datetime
             try:
                 # In case it's a RangeIndex or integer index that implies steps, we might not have real dates if they were dropped.
                 # However, FeatureEngineer usually sets the Date as index.
                 # If it failed, let's just use string representation or dummy dates.
                 df_features.index = pd.to_datetime(df_features.index)
             except:
                 pass
        
        if pd.api.types.is_datetime64_any_dtype(df_features.index):
             test_dates = df_features.index[-len(actuals):].strftime('%Y-%m-%d').tolist()
        else:
             # Fallback for non-datetime index
             test_dates = [str(x) for x in df_features.index[-len(actuals):].tolist()]

        # Metrics
        eval_metrics = evaluate_predictions(actuals, preds)
        
        # Risk Analysis
        risk_analyzer = RiskAnalyzer(actuals, preds)
        risk_metrics = risk_analyzer.get_risk_metrics()
        decision_score = risk_analyzer.risk_aware_decision_score(0, risk_metrics)
        
        # Construct Chart Data
        chart_data = []
        for i in range(len(test_dates)):
            chart_data.append({
                "date": test_dates[i],
                "actual": float(actuals[i]),
                "predicted": float(preds[i])
            })
            
        # Determine Volatility Label
        vol = risk_metrics.get('Annualized Volatility', 0)
        vol_label = "Low" if vol < 0.15 else "Medium" if vol < 0.3 else "High"
        
        return {
            "ticker": request.ticker,
            "model": model_name,
            "metrics": {
                "RMSE": eval_metrics.get('RMSE', 0.0),
                "MAPE": eval_metrics.get('MAPE', 0.0),
                "VaR_95": risk_metrics.get('VaR (95%)', 0.0),
                "Sharpe_Ratio": risk_metrics.get('Sharpe Ratio', 0.0),
                "Decision_Score": decision_score,
                "Volatility": vol_label
            },
            "chart_data": chart_data,
            "current_price": float(actuals[-1]) if len(actuals) > 0 else 0.0,
            "predicted_high": float(max(preds)) if len(preds) > 0 else 0.0
        }

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8081, reload=True)
