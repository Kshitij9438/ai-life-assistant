"""
Responsibility:
Defines machine learning models used for prediction tasks.
"""

from typing import List
import numpy as np


class LinearRegressionModel:
    """
    Simple linear regression model using ordinary least squares.
    """

    def __init__(self):
        self._weights: np.ndarray | None = None

    def fit(self, X: List[List[float]], y: List[float]) -> None:
        """
        Fit the model to training data.
        """
        if not X or not y:
            raise ValueError("Training data cannot be empty.")

        if len(X) != len(y):
            raise ValueError("X and y must have the same number of samples.")

        # Convert to NumPy arrays
        X_mat = np.array(X, dtype=float)
        y_vec = np.array(y, dtype=float)

        # Add bias term (column of ones)
        ones = np.ones((X_mat.shape[0], 1))
        X_design = np.hstack([ones, X_mat])

        # Closed-form solution: (XᵀX)^(-1) Xᵀ y
        XtX = X_design.T @ X_design

        # Use pseudo-inverse for numerical stability
        XtX_inv = np.linalg.pinv(XtX)

        self._weights = XtX_inv @ X_design.T @ y_vec

    def predict(self, X: List[List[float]]) -> List[float]:
        """
        Predict target values for given feature matrix.
        """
        if self._weights is None:
            raise RuntimeError("Model must be fitted before prediction.")

        X_mat = np.array(X, dtype=float)
        ones = np.ones((X_mat.shape[0], 1))
        X_design = np.hstack([ones, X_mat])

        predictions = X_design @ self._weights
        return predictions.tolist()

    def coefficients(self) -> List[float]:
        """
        Return learned model coefficients.
        """
        if self._weights is None:
            raise RuntimeError("Model has not been fitted yet.")

        return self._weights.tolist()
