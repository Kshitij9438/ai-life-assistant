from datetime import datetime, timedelta

from core.activity import Activity
from core.user import User
from ml.evaluate_weekly_model import evaluate_weekly_baseline


def _make_user_with_constant_weeks(weeks: int, minutes_per_day: int) -> User:
    """
    Creates a user with `weeks` full weeks of constant activity.
    """
    user = User("test_user")
    today = datetime.utcnow().date()

    total_days = weeks * 7
    for i in range(total_days):
        day = today - timedelta(days=(total_days - i))
        activity = Activity(
            name="Work",
            category="Work",
            duration_minutes=minutes_per_day,
            timestamp=datetime.combine(day, datetime.min.time()),
        )
        user.log_activity(activity)

    return user


def test_insufficient_data_returns_empty():
    user = _make_user_with_constant_weeks(1, 60)
    y_true, y_pred = evaluate_weekly_baseline(user)

    assert y_true == []
    assert y_pred == []


def test_exact_two_weeks_produces_one_prediction():
    user = _make_user_with_constant_weeks(2, 60)
    y_true, y_pred = evaluate_weekly_baseline(user)

    assert len(y_true) == 1
    assert len(y_pred) == 1


def test_constant_activity_baseline_correct():
    user = _make_user_with_constant_weeks(3, 60)

    y_true, y_pred = evaluate_weekly_baseline(user)

    # Each week: 7 × 60 = 420
    assert y_pred == [420.0, 420.0]
    assert y_true == [420.0, 420.0]
