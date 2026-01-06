"""
Responsibility:
Coordinates model training workflows.
"""

from typing import List, Dict, Tuple

from analytics.statistics import (
    activity_variability,
    category_balance,
    dominance_ratio,
)
from pipelines.week_utils import split_into_weeks


def build_weekly_training_data(user) -> Tuple[List[Dict[str, float]], List[float]]:
    """
    Build supervised learning data from a user's activity history.

    Each training example represents:
    - X[i]: Aggregated features from week i
    - y[i]: Total active minutes in week i+1
    """

    if user is None:
        return [], []

    # ---- Build daily totals ----
    daily_totals: Dict[str, int] = {
        log.get_date().isoformat(): log.total_duration()
        for log in user.get_all_logs()
    }

    if len(daily_totals) < 14:
        return [], []

    # ---- Split weeks ----
    current_week, previous_week = split_into_weeks(daily_totals)

    if not current_week or not previous_week:
        return [], []

    # ---- Category totals for current week ----
    weekly_category_totals: Dict[str, int] = {}

    for log in user.get_all_logs():
        date_str = log.get_date().isoformat()
        if date_str in current_week:
            for activity in log.get_activities():
                cat = activity.get_category()
                weekly_category_totals[cat] = (
                    weekly_category_totals.get(cat, 0)
                    + activity.get_duration_minutes()
                )

    values = list(current_week.values())

    features = {
    "total_minutes": float(sum(values)),
    "avg_daily_minutes": float(sum(values) / 7),
    "active_days": float(sum(1 for v in values if v > 0)),
    "max_day_minutes": float(max(values)),
    "min_day_minutes": float(min(values)),
    "daily_variability": float(activity_variability(current_week)),

    # ✅ FIXED SEMANTICS
    "category_balance": (
        1.0
        if len(weekly_category_totals) == 1
        else float(category_balance(weekly_category_totals))
    ),

    "dominance_ratio": float(dominance_ratio(current_week)),
    "category_dominance_ratio": float(
        dominance_ratio(weekly_category_totals)
    ),
}



    target = float(sum(previous_week.values()))

    return [features], [target]
