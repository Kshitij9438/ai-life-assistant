"""
Responsibility:
Runs analytics over a User's activity data and returns structured results.
"""

from typing import Dict, Any

from core.user import User
from analytics.aggregations import (
    total_duration_per_day,
    daily_category_minutes,
    total_duration_per_category,
)
from analytics.statistics import (
    daily_average,
    activity_variability,
)


def analyze_user(user: User) -> Dict[str, Any]:
    """
    Analyze a user's activity data and return aggregated analytics.

    Args:
        user: User domain object

    Returns:
        Dictionary containing analytics outputs.
    """
    # Convert domain objects → log dictionaries
    logs = []

    for day_log in user.get_all_logs():
        logs.append(
            {
                "date": day_log.get_date().isoformat(),
                "activities": [
                    {
                        "category": a.get_category(),
                        "duration_minutes": a.get_duration_minutes(),
                    }
                    for a in day_log.get_activities()
                ],
            }
        )

    daily_totals = total_duration_per_day(logs)
    daily_categories = daily_category_minutes(logs)
    category_totals = total_duration_per_category(logs)

    return {
        "daily_totals": daily_totals,
        "daily_categories": daily_categories,
        "category_totals": category_totals,
        "daily_average": daily_average(daily_totals),
        "variability": activity_variability(daily_totals),
    }
