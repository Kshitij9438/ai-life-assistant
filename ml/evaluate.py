"""
Responsibility:
Evaluates trained models using appropriate metrics.
"""

from typing import List
import math


def mean_absolute_error(y_true: List[float], y_pred: List[float]) -> float:
    """
    Compute Mean Absolute Error (MAE).
    """
    if len(y_true) != len(y_pred):
        raise ValueError("y_true and y_pred must have the same length.")

    return sum(abs(t - p) for t, p in zip(y_true, y_pred)) / len(y_true)


def root_mean_squared_error(y_true: List[float], y_pred: List[float]) -> float:
    """
    Compute Root Mean Squared Error (RMSE).
    """
    if len(y_true) != len(y_pred):
        raise ValueError("y_true and y_pred must have the same length.")

    mse = sum((t - p) ** 2 for t, p in zip(y_true, y_pred)) / len(y_true)
    return math.sqrt(mse)
