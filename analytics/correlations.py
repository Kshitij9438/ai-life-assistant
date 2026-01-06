"""
Responsibility:
Computes simple correlations between activity dimensions.
All functions are pure and operate on numeric inputs.
"""

from typing import Dict, List, Optional
import math


# -----------------------------
# Core math
# -----------------------------

def _pearson_correlation(x: List[float], y: List[float]) -> Optional[float]:
    if len(x) != len(y) or len(x) < 2:
        return None

    mean_x = sum(x) / len(x)
    mean_y = sum(y) / len(y)

    num = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y))
    den_x = sum((xi - mean_x) ** 2 for xi in x)
    den_y = sum((yi - mean_y) ** 2 for yi in y)

    if den_x == 0 or den_y == 0:
        return None

    return num / math.sqrt(den_x * den_y)


# -----------------------------
# Public API
# -----------------------------

def category_total_correlation(
    daily_category_minutes: Dict[str, Dict[str, int]],
    total_minutes_per_day: Dict[str, int],
) -> Dict[str, Optional[float]]:
    """
    Correlate per-category daily minutes with total daily activity.

    Args:
        daily_category_minutes:
            {
                "2026-01-01": {"Work": 120, "Study": 60, ...},
                ...
            }
        total_minutes_per_day:
            {
                "2026-01-01": 300,
                ...
            }

    Returns:
        Mapping of category -> correlation coefficient
    """
    correlations: Dict[str, Optional[float]] = {}

    if not daily_category_minutes or not total_minutes_per_day:
        return correlations

    # Ensure consistent day ordering
    days = sorted(set(daily_category_minutes) & set(total_minutes_per_day))

    if len(days) < 2:
        return correlations

    totals = [total_minutes_per_day[d] for d in days]

    # Collect per-category series
    category_series: Dict[str, List[float]] = {}

    for day in days:
        for category, minutes in daily_category_minutes[day].items():
            category_series.setdefault(category, []).append(minutes)

    for category, series in category_series.items():
        correlations[category] = _pearson_correlation(series, totals)

    return correlations
