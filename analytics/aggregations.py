"""
Responsibility:
Provides functions to aggregate activity data over time and categories.
All functions operate on raw log dictionaries.
"""

from typing import Dict, List


# -----------------------------
# Daily aggregations
# -----------------------------

def total_duration_per_day(logs: List[dict]) -> Dict[str, int]:
    """
    Compute total activity duration per day.

    Returns:
        { "YYYY-MM-DD": total_minutes }
    """
    totals: Dict[str, int] = {}

    for log in logs:
        date = log["date"]
        activities = log.get("activities", [])
        totals[date] = sum(a["duration_minutes"] for a in activities)

    return totals


def daily_category_minutes(logs: List[dict]) -> Dict[str, Dict[str, int]]:
    """
    Compute per-category activity duration for each day.

    Returns:
        {
            "YYYY-MM-DD": {
                "Work": minutes,
                "Study": minutes,
                ...
            }
        }
    """
    result: Dict[str, Dict[str, int]] = {}

    for log in logs:
        date = log["date"]
        result[date] = {}

        for activity in log.get("activities", []):
            category = activity["category"]
            duration = activity["duration_minutes"]

            result[date][category] = (
                result[date].get(category, 0) + duration
            )

    return result


# -----------------------------
# Cross-day aggregations
# -----------------------------

def total_duration_per_category(logs: List[dict]) -> Dict[str, int]:
    """
    Compute total activity duration per category across all days.
    """
    totals: Dict[str, int] = {}

    for log in logs:
        for activity in log.get("activities", []):
            category = activity["category"]
            duration = activity["duration_minutes"]
            totals[category] = totals.get(category, 0) + duration

    return totals


def activity_count_per_category(logs: List[dict]) -> Dict[str, int]:
    """
    Count number of activities per category across all days.
    """
    counts: Dict[str, int] = {}

    for log in logs:
        for activity in log.get("activities", []):
            category = activity["category"]
            counts[category] = counts.get(category, 0) + 1

    return counts
