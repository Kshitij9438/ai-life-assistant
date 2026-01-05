"""
Responsibility:
Generates human-readable summaries of system insights.
"""

from typing import Dict


def _minutes_to_hm(minutes: int) -> str:
    hours = minutes // 60
    mins = minutes % 60
    return f"{hours}h {mins}m"


def summarize_daily_activity(category_totals: Dict[str, int]) -> str:
    """
    Generate a human-readable insight summary for a single day.

    Args:
        category_totals: Mapping of category to total minutes.

    Returns:
        A natural language summary string.
    """
    if not category_totals:
        return "No activity data available for this day."

    total_minutes = sum(category_totals.values())

    # Sort categories by time spent (descending)
    sorted_categories = sorted(
        category_totals.items(), key=lambda x: x[1], reverse=True
    )

    top_category, top_minutes = sorted_categories[0]
    share = top_minutes / total_minutes

    lines = []

    lines.append(
        f"Your highest time investment was in **{top_category}** "
        f"({_minutes_to_hm(top_minutes)})."
    )

    if share >= 0.6:
        lines.append(
            f"This category dominated your day, accounting for most of your active time."
        )
    elif share >= 0.4:
        lines.append(
            f"This category was a major focus, but your time was still distributed across other areas."
        )
    else:
        lines.append(
            f"Your time was fairly balanced across multiple categories."
        )

    # Optional secondary insight
    if len(sorted_categories) > 1:
        second_category, second_minutes = sorted_categories[1]
        lines.append(
            f"The next largest time block was **{second_category}** "
            f"({_minutes_to_hm(second_minutes)})."
        )

    return " ".join(lines)
def summarize_weekly_trend(
    current_total: int,
    previous_total: int,
) -> str:
    """
    Generate a human-readable summary comparing weekly activity totals.
    """
    if previous_total == 0:
        return (
            "Not enough data from the previous week to assess trends."
        )

    diff = current_total - previous_total
    percent_change = (diff / previous_total) * 100

    if abs(percent_change) < 5:
        return (
            "Your overall activity level remained fairly consistent compared to last week."
        )

    if percent_change > 0:
        return (
            f"Your activity increased by {percent_change:.1f}% compared to last week, "
            f"indicating higher overall engagement."
        )

    return (
        f"Your activity decreased by {abs(percent_change):.1f}% compared to last week. "
        f"This could indicate a lighter workload or more rest."
    )
