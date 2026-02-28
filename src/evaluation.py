import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error

def mean_absolute_percentage_error(y_true, y_pred): 
    return np.mean(np.abs((y_true - y_pred) / y_true)) * 100

def directional_accuracy(y_true, y_pred):
    # Compares direction of change
    true_diff = np.diff(y_true)
    pred_diff = np.diff(y_pred)
    # Check if sign matches
    matches = (np.sign(true_diff) == np.sign(pred_diff))
    return np.mean(matches) * 100

def evaluate_predictions(y_true, y_pred):
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    mae = mean_absolute_error(y_true, y_pred)
    mape = mean_absolute_percentage_error(y_true, y_pred)
    da = directional_accuracy(y_true, y_pred)
    
    return {
        "RMSE": rmse,
        "MAE": mae,
        "MAPE": mape,
        "Directional Accuracy (%)": da
    }
