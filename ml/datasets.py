"""
Responsibility:
Builds training and evaluation datasets from extracted features.
"""

from typing import Dict, List, Tuple


def extract_feature_names(X: List[Dict[str, float]]) -> List[str]:
    """
    Extract ordered feature names from feature dictionaries.
    """
    if not X:
        raise ValueError("X must contain at least one feature dictionary.")

    # Use sorted keys to ensure deterministic ordering
    return sorted(X[0].keys())


def vectorize_features(
    X: List[Dict[str, float]],
    feature_names: List[str],
) -> List[List[float]]:
    """
    Convert feature dictionaries into numeric vectors.
    """
    vectors: List[List[float]] = []

    for row in X:
        vector = [float(row.get(name, 0.0)) for name in feature_names]
        vectors.append(vector)

    return vectors


def train_test_split(
    X: List[List[float]],
    y: List[float],
    test_ratio: float = 0.2,
) -> Tuple[List[List[float]], List[List[float]], List[float], List[float]]:
    """
    Split dataset into train and test sets without shuffling.
    """
    if len(X) != len(y):
        raise ValueError("X and y must have the same length.")

    if not 0.0 < test_ratio < 1.0:
        raise ValueError("test_ratio must be between 0 and 1.")

    n = len(X)
    split_index = int(n * (1 - test_ratio))

    X_train = X[:split_index]
    X_test = X[split_index:]
    y_train = y[:split_index]
    y_test = y[split_index:]

    return X_train, X_test, y_train, y_test
