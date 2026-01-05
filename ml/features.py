"""
Responsibility:
Transforms structured activity data into machine learning features.
"""

from typing import Dict, List, Tuple
from datetime import datetime


def extract_daily_features(log: dict) -> Dict[str, float]:
    """
    Extract numerical features from a single day's log.

    Args:
        log: A single day log dictionary.

    Returns:
        Mapping of feature name to value.
    """
    activities = log.get("activities", [])

    features: Dict[str, float] = {}

    total_minutes = 0
    activity_count = len(activities)

    # Initialize category totals
    category_totals: Dict[str, int] = {}

    for activity in activities:
        duration = activity["duration_minutes"]
        category = activity["category"]

        total_minutes += duration
        category_totals[category] = category_totals.get(category, 0) + duration

    # Core features
    features["total_minutes"] = total_minutes
    features["activity_count"] = activity_count

    # Category-specific features (safe even if missing)
    for category in ["Work", "Study", "Health", "Leisure"]:
        features[f"{category.lower()}_minutes"] = category_totals.get(category, 0)

    # Temporal feature
    date_obj = datetime.fromisoformat(log["date"])
    features["day_of_week"] = float(date_obj.weekday())

    return features


def build_feature_matrix(
    logs: List[dict],
) -> Tuple[List[Dict[str, float]], List[float]]:
    """
    Build feature matrix X and target vector y for ML.

    Args:
        logs: List of day log dictionaries sorted by date ascending.

    Returns:
        X: List of feature dictionaries
        y: List of target values (next day's total minutes)
    """
    X: List[Dict[str, float]] = []
    y: List[float] = []

    # Precompute total minutes per day
    daily_totals = [
        sum(a["duration_minutes"] for a in log.get("activities", []))
        for log in logs
    ]

    for i in range(len(logs) - 1):
        features = extract_daily_features(logs[i])

        # --- Lag features ---
        features["prev_day_total_minutes"] = (
            daily_totals[i - 1] if i - 1 >= 0 else 0.0
        )

        features["avg_last_3_days_minutes"] = (
            sum(daily_totals[max(0, i - 3):i]) / max(1, i)
            if i > 0 else 0.0
        )

        features["avg_last_7_days_minutes"] = (
            sum(daily_totals[max(0, i - 7):i]) / max(1, i)
            if i > 0 else 0.0
        )

        # Target: tomorrow's total
        target = daily_totals[i + 1]

        X.append(features)
        y.append(float(target))

    return X, y

