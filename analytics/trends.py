"""
Responsibility:
Analyzes temporal patterns and changes in activity behavior.
"""

from typing import Dict, List, Tuple


def split_weeks(logs: List[dict]) -> Tuple[List[dict], List[dict]]:
    """
    Split logs into current week and previous week.

    Args:
        logs: List of day log dictionaries sorted by date descending.

    Returns:
        A tuple of (current_week_logs, previous_week_logs).
    """
    current_week = logs[:7]
    previous_week = logs[7:14]
    return current_week, previous_week


def weekly_total_duration(logs: List[dict]) -> int:
    """
    Compute total activity duration for a set of logs.
    """
    total = 0
    for log in logs:
        for activity in log.get("activities", []):
            total += activity["duration_minutes"]
    return total


def weekly_category_totals(logs: List[dict]) -> Dict[str, int]:
    """
    Compute total duration per category for a week.
    """
    totals: Dict[str, int] = {}

    for log in logs:
        for activity in log.get("activities", []):
            category = activity["category"]
            duration = activity["duration_minutes"]
            totals[category] = totals.get(category, 0) + duration

    return totals
