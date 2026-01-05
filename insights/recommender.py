"""
Responsibility:
Combines analytics outputs to generate actionable recommendations.
"""

from typing import Dict, List


def recommend_from_daily_activity(category_totals: Dict[str, int]) -> List[str]:
    """
    Generate actionable recommendations based on daily activity distribution.

    Args:
        category_totals: Mapping of category to total minutes.

    Returns:
        A list of recommendation strings.
    """
    recommendations: List[str] = []

    if not category_totals:
        return recommendations

    total_minutes = sum(category_totals.values())
    avg_minutes = total_minutes / len(category_totals)

    # Identify under-invested categories
    for category, minutes in category_totals.items():
        if minutes < 0.5 * avg_minutes:
            recommendations.append(
                f"You spent relatively little time on {category}. "
                f"Consider allocating a focused block for it tomorrow."
            )

    # Identify dominant category
    top_category = max(category_totals, key=category_totals.get)
    top_share = category_totals[top_category] / total_minutes

    if top_share >= 0.6:
        recommendations.append(
            f"{top_category} dominated your day. "
            f"If this continues, consider balancing it with lighter activities."
        )

    # If everything is balanced
    if not recommendations:
        recommendations.append(
            "Your time distribution today was fairly balanced. "
            "Maintaining this balance can help sustain productivity."
        )

    return recommendations
def recommend_from_weekly_trend(
    current_total: int,
    previous_total: int,
) -> list[str]:
    """
    Generate recommendations based on weekly activity trends.
    """
    recommendations: list[str] = []

    if previous_total == 0:
        return recommendations

    diff = current_total - previous_total
    percent_change = (diff / previous_total) * 100

    # Significant decrease
    if percent_change <= -10:
        recommendations.append(
            "Your overall activity dropped noticeably compared to last week. "
            "If this was unintentional, consider planning lighter but consistent activity blocks."
        )

    # Moderate decrease
    elif -10 < percent_change <= -5:
        recommendations.append(
            "Your activity was slightly lower than last week. "
            "A small adjustment in routine could help regain momentum."
        )

    # Significant increase
    elif percent_change >= 10:
        recommendations.append(
            "Your activity increased significantly this week. "
            "Make sure the pace feels sustainable and allows for recovery."
        )

    # Moderate increase
    elif 5 <= percent_change < 10:
        recommendations.append(
            "You were slightly more active than last week. "
            "If this felt good, maintaining this level could be beneficial."
        )

    # Stable
    else:
        recommendations.append(
            "Your weekly activity level has remained stable. "
            "Consistency like this is often a strong foundation for long-term progress."
        )

    return recommendations
