"""
Responsibility:
Trains an interpretable weekly activity prediction model.
"""

from typing import Dict, List, Tuple

from ml.models import LinearRegressionModel
from ml.datasets import extract_feature_names, vectorize_features
from ml.train import build_weekly_training_data


def train_weekly_model(user) -> Tuple[LinearRegressionModel, Dict[str, float]]:
    """
    Train a linear regression model to predict next week's activity.

    Returns:
        model: trained LinearRegressionModel
        coefficients: { feature_name: coefficient }
    """
    # 1. Build training data
    X_dicts, y = build_weekly_training_data(user)

    if not X_dicts:
        raise ValueError("Not enough data to train weekly model.")

    # 2. Vectorize features
    feature_names = extract_feature_names(X_dicts)
    X = vectorize_features(X_dicts, feature_names)

    # 3. Train model
    model = LinearRegressionModel()
    model.fit(X, y)

    # 4. Map coefficients to feature names
    coefficients = dict(zip(feature_names, model.coefficients()))

    return model, coefficients
