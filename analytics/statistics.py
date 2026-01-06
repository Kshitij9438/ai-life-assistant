"""
Responsibility:
Provides statistical utilities for analyzing activity data.
All functions are pure and operate on numeric inputs only.
"""

from typing import Dict, List, Optional
import math
from typing import Dict



# -----------------------------
# Basic statistics
# -----------------------------

def mean(values: List[float]) -> Optional[float]:
    if not values:
        return None
    return sum(values) / len(values)


def variance(values: List[float]) -> Optional[float]:
    if not values:
        return None

    avg = mean(values)
    return sum((x - avg) ** 2 for x in values) / len(values)


def standard_deviation(values: List[float]) -> Optional[float]:
    var = variance(values)
    if var is None:
        return None
    return math.sqrt(var)


# -----------------------------
# Activity-specific helpers
# -----------------------------

def daily_average(total_minutes_per_day: Dict[str, int]) -> Optional[float]:
    """
    Compute average daily activity duration.
    """
    return mean(list(total_minutes_per_day.values()))


def activity_variability(total_minutes_per_day: Dict[str, int]) -> Optional[float]:
    """
    Measure how consistent daily activity levels are.
    Higher value => more fluctuation.
    """
    return standard_deviation(list(total_minutes_per_day.values()))


def category_share(category_minutes: Dict[str, int]) -> Dict[str, float]:
    """
    Compute proportional share of time spent per category.
    """
    total = sum(category_minutes.values())

    if total == 0:
        return {k: 0.0 for k in category_minutes}

    return {
        category: minutes / total
        for category, minutes in category_minutes.items()
    }

def category_balance(category_minutes: Dict[str, int]) -> float:
    """
    Measure how evenly time is distributed across categories.
    Returns a value between 0.0 (single category dominates)
    and 1.0 (perfectly balanced).
    """
    if not category_minutes:
        return 0.0

    total = sum(category_minutes.values())
    if total == 0:
        return 0.0

    proportions = [
        minutes / total
        for minutes in category_minutes.values()
        if minutes > 0
    ]

    if len(proportions) <= 1:
        return 0.0

    entropy = -sum(p * math.log(p) for p in proportions)
    max_entropy = math.log(len(proportions))

    return entropy / max_entropy
def dominance_ratio(category_minutes: Dict[str, int]) -> float:
    """
    Measures how dominant the top category is.
    Returns a value between 0.0 and 1.0.
    """
    if not category_minutes:
        return 0.0

    total = sum(category_minutes.values())
    if total == 0:
        return 0.0

    return max(category_minutes.values()) / total
