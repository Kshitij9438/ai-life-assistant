"""
Responsibility:
Runs the daily analytics and insight generation pipeline.
"""

import json
from pathlib import Path
from typing import Dict

from analytics.aggregations import total_duration_per_day
from insights.summary import summarize_daily_activity
from insights.recommender import recommend_from_daily_activity

from ml.features import build_feature_matrix
from ml.datasets import extract_feature_names, vectorize_features, train_test_split
from ml.models import LinearRegressionModel


def _minutes_to_hours(minutes: float) -> str:
    hours = minutes / 60.0
    return f"{hours:.1f} hours"


def _minutes_to_hm(minutes: int) -> str:
    hours = minutes // 60
    mins = minutes % 60
    return f"{hours}h {mins}m"


def run_daily_report(date_str: str) -> None:
    """
    Generate and print a daily activity report for a given date.
    """
    data_path = Path("data/synthetic/synthetic_user.json")

    if not data_path.exists():
        raise FileNotFoundError("Synthetic data file not found.")

    with data_path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    logs = data["logs"]

    # --- ML prediction: tomorrow's total activity ---
    logs_sorted = sorted(logs, key=lambda x: x["date"])
    predicted_minutes = None

    try:
        X_dicts, y = build_feature_matrix(logs_sorted)

        if len(X_dicts) >= 5:
            feature_names = extract_feature_names(X_dicts)
            X = vectorize_features(X_dicts, feature_names)

            X_train, X_test, y_train, y_test = train_test_split(X, y)

            model = LinearRegressionModel()
            model.fit(X_train, y_train)

            # Predict using the most recent day
            predicted_minutes = model.predict(X[-1:])[0]

    except Exception:
        predicted_minutes = None

    # --- Daily analytics ---
    day_log = next((log for log in logs if log["date"] == date_str), None)

    if day_log is None:
        raise ValueError(f"No data found for date {date_str}.")

    activities = day_log.get("activities", [])
    total_minutes = sum(a["duration_minutes"] for a in activities)

    category_totals: Dict[str, int] = {}
    for activity in activities:
        category = activity["category"]
        duration = activity["duration_minutes"]
        category_totals[category] = category_totals.get(category, 0) + duration

    # ---- Output ----
    print(f"\n📅 Daily Report — {date_str}\n")
    print(f"Total active time: {_minutes_to_hm(total_minutes)}\n")
    print("By category:")

    for category, minutes in sorted(category_totals.items()):
        print(f"- {category}: {_minutes_to_hm(minutes)}")

    print("\n🧠 Insight:")
    print(summarize_daily_activity(category_totals))

    print("\n💡 Recommendations:")
    for rec in recommend_from_daily_activity(category_totals):
        print(f"- {rec}")

    if predicted_minutes is not None:
        print("\n🔮 Prediction:")
        print(
            f"Estimated total activity for tomorrow: "
            f"{_minutes_to_hours(predicted_minutes)}"
        )


if __name__ == "__main__":
    run_daily_report(date_str="2026-01-06")
