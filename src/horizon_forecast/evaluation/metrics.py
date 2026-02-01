import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error

def smape(y_true, y_pred):
    denom = (np.abs(y_true) + np.abs(y_pred)) / 2
    diff = np.abs(y_true - y_pred)
    return np.mean(diff / (denom + 1e-6)) * 100

def mae_percent(y_true, y_pred):
    return (mean_absolute_error(y_true, y_pred) / (np.mean(y_true) + 1e-6)) * 100

def bias(y_true, y_pred):
    return np.mean(y_pred - y_true)

def regression_metrics(y_true, y_pred):
    mae = mean_absolute_error(y_true, y_pred)
    mse = mean_squared_error(y_true, y_pred)
    rmse = np.sqrt(mse)
    mape = np.mean(np.abs((y_true - y_pred) / (y_true + 1e-6))) * 100
    smape_val = smape(y_true, y_pred)
    mae_pct = mae_percent(y_true, y_pred)
    bias_val = bias(y_true, y_pred)

    return {
        "MAE": mae,
        "RMSE": rmse,
        "MAPE": mape,
        "SMAPE": smape_val,
        "MAE%": mae_pct,
        "Bias": bias_val
    }