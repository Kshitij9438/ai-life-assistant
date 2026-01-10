"""
Responsibility:
Trains an interpretable weekly activity prediction model.
"""

from typing import Dict, Tuple

from ml.models import LinearRegressionModel
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
    if len(X_dicts) < 2:
        raise ValueError(
        "Weekly ML requires multiple samples to be evaluative. "
        "Current usage is illustrative only."
    )


    if not X_dicts:
        raise ValueError("Not enough data to train weekly model.")

    # 2. Extract feature ordering ONCE
    feature_names = list(X_dicts[0].keys())

    # 3. Train model
    model = LinearRegressionModel(feature_names)
    model.fit(X_dicts, y)

    # 4. Coefficients are already mapped correctly
    coefficients = model.coefficients()

    return model, coefficients
