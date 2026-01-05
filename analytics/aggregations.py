"""
Responsibility:
Provides functions to aggregate activity data over time and categories.
"""

from typing import Dict, List


def total_duration_per_day(logs: List[dict]) -> Dict[str, int]:
    """
    Compute total activity duration per day.

    Args:
        logs: List of day log dictionaries.

    Returns:
        Mapping of date string to total duration in minutes.
    """
    totals: Dict[str, int] = {}

    for log in logs:
        date = log["date"]
        activities = log.get("activities", [])

        day_total = sum(a["duration_minutes"] for a in activities)
        totals[date] = day_total

    return totals


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
    Count number of activities per category.
    """
    counts: Dict[str, int] = {}

    for log in logs:
        for activity in log.get("activities", []):
            category = activity["category"]
            counts[category] = counts.get(category, 0) + 1

    return counts
