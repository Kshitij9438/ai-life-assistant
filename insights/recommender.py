"""
Responsibility:
Generates actionable recommendations based on rule-derived signals.
"""

from typing import Dict, List

from analytics.statistics import category_share
from config.settings import UNDERREPRESENTED_CATEGORY_SHARE, DOMINANT_CATEGORY_SHARE
from config.constants import ALL_CATEGORIES


# -----------------------------
# Daily recommendations
# -----------------------------

def recommend_from_daily_activity(
    category_totals: Dict[str, int],
) -> List[str]:
    """
    Generate actionable recommendations based on daily activity patterns.
    """
    recommendations: List[str] = []

    if not category_totals:
        return recommendations

    total_minutes = sum(category_totals.values())
    if total_minutes == 0:
        return recommendations

    shares = category_share(category_totals)

    # Underrepresented categories → encourage action
    for category in ALL_CATEGORIES:
        share = shares.get(category, 0.0)
        if 0 < share < UNDERREPRESENTED_CATEGORY_SHARE:
            recommendations.append(
                f"You spent very little time on {category}. "
                f"Consider scheduling a short, focused session for it tomorrow."
            )

    # Dominant category → suggest balance
    for category, share in shares.items():
        if share >= DOMINANT_CATEGORY_SHARE:
            recommendations.append(
                f"{category} took up most of your day. "
                f"Balancing it with lighter or restorative activities may help sustainability."
            )

    if not recommendations:
        recommendations.append(
            "Your activity distribution today was well balanced. "
            "Maintaining this balance can support long-term consistency."
        )

    return recommendations


# -----------------------------
# Weekly recommendations
# -----------------------------

def recommend_from_weekly_trend(
    current_total: int,
    previous_total: int,
) -> List[str]:
    """
    Generate recommendations based on week-over-week activity trends.
    """
    recommendations: List[str] = []

    if previous_total == 0:
        return recommendations

    percent_change = ((current_total - previous_total) / previous_total) * 100

    if percent_change <= -10:
        recommendations.append(
            "Your overall activity dropped significantly compared to last week. "
            "If unintentional, consider planning smaller but consistent activity blocks."
        )

    elif -10 < percent_change <= -5:
        recommendations.append(
            "Your activity decreased slightly from last week. "
            "A minor routine adjustment could help restore momentum."
        )

    elif percent_change >= 10:
        recommendations.append(
            "Your activity increased substantially this week. "
            "Ensure the pace feels sustainable and includes adequate recovery."
        )

    elif 5 <= percent_change < 10:
        recommendations.append(
            "You were slightly more active than last week. "
            "If this felt manageable, maintaining this level could be beneficial."
        )

    else:
        recommendations.append(
            "Your weekly activity level remained stable. "
            "Consistency like this often supports long-term progress."
        )

    return recommendations
