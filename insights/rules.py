"""
Responsibility:
Defines rule-based insights derived from analytics outputs.
Rules are explicit, interpretable, and deterministic.
"""

from typing import Dict, List

from config.settings import (
    DOMINANT_CATEGORY_SHARE,
    UNDERREPRESENTED_CATEGORY_SHARE,
    MIN_ACTIVE_MINUTES_PER_DAY,
)
from config.constants import ALL_CATEGORIES


# -----------------------------
# Daily rules
# -----------------------------

def dominant_category_rules(
    category_shares: Dict[str, float],
) -> List[str]:
    """
    Identify whether a single category dominates the day.
    """
    messages: List[str] = []

    for category, share in category_shares.items():
        if share >= DOMINANT_CATEGORY_SHARE:
            messages.append(
                f"{category} dominated your day "
                f"({share:.0%} of total activity)."
            )

    return messages


def underrepresented_category_rules(
    category_shares: Dict[str, float],
) -> List[str]:
    """
    Identify categories that received very little attention.
    """
    messages: List[str] = []

    for category in ALL_CATEGORIES:
        share = category_shares.get(category, 0.0)
        if 0 < share < UNDERREPRESENTED_CATEGORY_SHARE:
            messages.append(
                f"You spent very little time on {category} today."
            )

    return messages


def low_activity_rule(total_minutes: int) -> List[str]:
    """
    Detect days with unusually low total activity.
    """
    if total_minutes < MIN_ACTIVE_MINUTES_PER_DAY:
        return [
            "Your total activity today was very low. "
            "This could indicate rest, burnout, or missing data."
        ]
    return []


# -----------------------------
# Weekly rules
# -----------------------------

def consistency_rule(
    variability: float,
    threshold: float = 60.0,
) -> List[str]:
    """
    Detect high variability in daily activity.
    """
    if variability >= threshold:
        return [
            "Your activity levels fluctuated significantly this week, "
            "indicating inconsistent routines."
        ]
    return []
