"""
Responsibility:
Generates insights and recommendations from analytics outputs.
"""

from typing import Dict, Any, List, Optional

from insights.summary import (
    summarize_daily_activity,
    summarize_weekly_trend,
)
from insights.recommender import (
    recommend_from_daily_activity,
    recommend_from_weekly_trend,
)
def _latest_day_category_totals(
    analysis: Dict[str, Any],
) -> Dict[str, int]:
    """
    Extract category totals for the most recent day only.
    """
    daily_categories = analysis.get("daily_categories", {})
    if not daily_categories:
        return {}

    latest_date = max(daily_categories.keys())
    return daily_categories.get(latest_date, {})


def generate_insights(
    analysis: Dict[str, Any],
    previous_week_total: Optional[int] = None,
) -> Dict[str, Any]:
    """
    Generate summaries and recommendations from analytics results.

    Args:
        analysis: Output from analyze_user
        previous_week_total: Optional total minutes from previous week

    Returns:
        Dictionary containing summaries and recommendations.
    """
    latest_day_categories = _latest_day_category_totals(analysis)
    daily_summary = summarize_daily_activity(latest_day_categories)
    daily_recommendations = recommend_from_daily_activity(latest_day_categories)

    weekly_summary: Optional[str] = None
    weekly_recommendations: List[str] = []

    if previous_week_total is not None:
        current_week_total = sum(
            analysis.get("daily_totals", {}).values()
        )

        weekly_summary = summarize_weekly_trend(
            current_week_total,
            previous_week_total,
        )

        weekly_recommendations = recommend_from_weekly_trend(
            current_week_total,
            previous_week_total,
        )

    return {
        "daily_summary": daily_summary,
        "daily_recommendations": daily_recommendations,
        "weekly_summary": weekly_summary,
        "weekly_recommendations": weekly_recommendations,
    }
