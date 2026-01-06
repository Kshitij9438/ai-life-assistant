from insights.summary import summarize_daily_activity
from insights.recommender import recommend_from_daily_activity


def test_summarize_daily_activity_basic():
    category_totals = {
        "Work": 180,
        "Study": 60,
        "Exercise": 30,
    }

    summary = summarize_daily_activity(category_totals)

    # Basic sanity checks
    assert isinstance(summary, str)
    assert len(summary) > 0

    # Semantic anchors
    assert "Work" in summary          # top category mentioned
    assert "h" in summary or "m" in summary  # time information present



def test_recommend_from_daily_activity_basic():
    category_totals = {
        "Work": 180,
        "Study": 30,
        "Exercise": 30,
    }

    recommendations = recommend_from_daily_activity(category_totals)

    assert isinstance(recommendations, list)
    assert len(recommendations) > 0
    assert any("Study" in r or "Exercise" in r for r in recommendations)
