"""
Responsibility:
Defines machine learning models used for prediction tasks.
"""

from typing import List, Dict
import numpy as np


class LinearRegressionModel:
    """
    Simple linear regression model using ordinary least squares.
    """

    def __init__(self, feature_names: List[str]):
        self._weights: np.ndarray | None = None
        self._feature_names = feature_names

    def _vectorize(self, X: List[Dict[str, float]]) -> np.ndarray:
        """
        Convert list of feature dictionaries into a numeric matrix
        using a fixed feature ordering.
        """
        return np.array(
            [[x[name] for name in self._feature_names] for x in X],
            dtype=float,
        )

    def fit(self, X: List[Dict[str, float]], y: List[float]) -> None:
        """
        Fit the model to training data.
        """
        if not X or not y:
            raise ValueError("Training data cannot be empty.")

        if len(X) != len(y):
            raise ValueError("X and y must have the same number of samples.")

        X_mat = self._vectorize(X)
        y_vec = np.array(y, dtype=float)

        # Add bias term
        ones = np.ones((X_mat.shape[0], 1))
        X_design = np.hstack([ones, X_mat])

        # Closed-form OLS
        XtX = X_design.T @ X_design
        XtX_inv = np.linalg.pinv(XtX)

        self._weights = XtX_inv @ X_design.T @ y_vec

    def predict(self, X: List[Dict[str, float]]) -> List[float]:
        """
        Predict target values for given feature dictionaries.
        """
        if self._weights is None:
            raise RuntimeError("Model must be fitted before prediction.")

        X_mat = self._vectorize(X)
        ones = np.ones((X_mat.shape[0], 1))
        X_design = np.hstack([ones, X_mat])

        return (X_design @ self._weights).tolist()

    def coefficients(self) -> Dict[str, float]:
        """
        Return learned coefficients mapped to feature names.
        """
        if self._weights is None:
            raise RuntimeError("Model has not been fitted yet.")

        coef = self._weights[1:]  # skip bias
        return dict(zip(self._feature_names, coef.tolist()))

    def intercept(self) -> float:
        if self._weights is None:
            raise RuntimeError("Model has not been fitted yet.")
        return float(self._weights[0])
