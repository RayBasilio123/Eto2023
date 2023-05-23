import os
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error


def calculate_rmse(y_true, y_pred):
    """
    Calcula o Root Mean Square Error (RMSE).

    Args:
        y_true: Array com os valores observados.
        y_pred: Array com os valores preditos.

    Returns:
        O valor do RMSE.
    """
    mse = mean_squared_error(y_true, y_pred)
    rmse = np.sqrt(mse)
    return round(rmse, 2)

def calculate_mae(y_true, y_pred):
    """
    Calcula o Mean Absolute Error (MAE).

    Args:
        y_true: Array com os valores observados.
        y_pred: Array com os valores preditos.

    Returns:
        O valor do MAE.
    """
    mae = mean_absolute_error(y_true, y_pred)
    return round(mae, 2)

def calculate_nse(y_true, y_pred):
    """
    Calcula o Nash-Sutcliffe Efficiency (NSE).

    Args:
        y_true: Array com os valores observados.
        y_pred: Array com os valores preditos.

    Returns:
        O valor do NSE.
    """
    nse = 1 - (np.sum((y_true - y_pred) ** 2) / np.sum((y_true - np.mean(y_true)) ** 2))
    return round(nse, 2)

def calculate_mbe(y_true, y_pred):
    """
    Calcula o Mean Bias Error (MBE).

    Args:
        y_true: Array com os valores observados.
        y_pred: Array com os valores preditos.

    Returns:
        O valor do MBE.
    """
    mbe = np.mean(y_true - y_pred)
    return  round(mbe, 2)

