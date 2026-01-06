"""
Responsibility:
Generates human-readable summaries of system insights.
This module orchestrates rule outputs into coherent narratives.
"""

from typing import Dict, List

from analytics.statistics import category_share
from insights.rules import (
    dominant_category_rules,
    underrepresented_category_rules,
    low_activity_rule,
)


# -----------------------------
# Helpers
# -----------------------------

def _minutes_to_hm(minutes: int) -> str:
    hours = minutes // 60
    mins = minutes % 60
    return f"{hours}h {mins}m"


# -----------------------------
# Daily summary
# -----------------------------

def summarize_daily_activity(category_totals: Dict[str, int]) -> str:
    """
    Generate a human-readable insight summary for a single day.
    """
    if not category_totals:
        return "No activity data available for this day."

    total_minutes = sum(category_totals.values())
    category_shares = category_share(category_totals)

    lines: List[str] = []

    # High-level overview
    top_category = max(category_totals, key=category_totals.get)
    top_minutes = category_totals[top_category]

    lines.append(
        f"Your highest time investment was in **{top_category}** "
        f"({_minutes_to_hm(top_minutes)})."
    )

    # Apply rules
    lines.extend(dominant_category_rules(category_shares))
    lines.extend(underrepresented_category_rules(category_shares))
    lines.extend(low_activity_rule(total_minutes))

    return " ".join(lines)


# -----------------------------
# Weekly summary
# -----------------------------

def summarize_weekly_trend(
    current_total: int,
    previous_total: int,
) -> str:
    """
    Generate a human-readable summary comparing weekly activity totals.
    """
    if previous_total == 0:
        return "Not enough data from the previous week to assess trends."

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
