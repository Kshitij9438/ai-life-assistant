"""
Responsibility:
Runs the daily analytics and observational insight pipeline.

NOTE:
Daily intelligence is descriptive and reflective only.
No predictive ML is performed at daily resolution (v1 doctrine).
"""

import json
from pathlib import Path
from typing import Dict

from insights.summary import summarize_daily_activity
from insights.recommender import recommend_from_daily_activity


def _minutes_to_hm(minutes: int) -> str:
    hours = minutes // 60
    mins = minutes % 60
    return f"{hours}h {mins}m"


def run_daily_report(date_str: str) -> None:
    """
    Generate and print a daily activity report for a given date.

    This function provides:
    - factual summaries
    - qualitative insights
    - behavioral recommendations

    It explicitly does NOT produce predictions.
    """

    data_path = Path("data/synthetic/synthetic_user.json")

    if not data_path.exists():
        raise FileNotFoundError("Synthetic data file not found.")

    with data_path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    logs = data["logs"]

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

    print("\n🧠 Daily Insight:")
    print(summarize_daily_activity(category_totals))

    print("\n💡 Recommendations:")
    for rec in recommend_from_daily_activity(category_totals):
        print(f"- {rec}")

    print(
        "\nℹ️ Note: Daily predictions are intentionally withheld. "
        "Weekly intelligence provides forecasted insights with confidence and context."
    )


if __name__ == "__main__":
    run_daily_report(date_str="2026-01-06")
