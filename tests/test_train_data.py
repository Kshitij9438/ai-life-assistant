from datetime import datetime, timedelta

from core.activity import Activity
from core.user import User
from ml.train import build_weekly_training_data


def _make_user_with_n_days(n: int) -> User:
    user = User("test_user")
    today = datetime.utcnow().date()

    for i in range(n):
        day = today - timedelta(days=(n - i))
        activity = Activity(
            name="Work",
            category="Work",
            duration_minutes=60,
            timestamp=datetime.combine(day, datetime.min.time()),
        )
        user.log_activity(activity)

    return user


def test_insufficient_data_returns_empty():
    user = _make_user_with_n_days(10)
    X, y = build_weekly_training_data(user)

    assert X == []
    assert y == []


def test_exact_two_weeks_produces_one_sample():
    user = _make_user_with_n_days(14)
    X, y = build_weekly_training_data(user)

    assert len(X) == 1
    assert len(y) == 1


def test_feature_values_correctness():
    user = _make_user_with_n_days(14)
    X, y = build_weekly_training_data(user)

    features = X[0]

    assert features["total_minutes"] == 420.0   # 7 days × 60
    assert features["avg_daily_minutes"] == 60.0
    assert features["active_days"] == 7.0
    assert features["max_day_minutes"] == 60.0
    assert features["min_day_minutes"] == 60.0


def test_target_is_next_week_total():
    user = _make_user_with_n_days(14)
    X, y = build_weekly_training_data(user)

    assert y[0] == 420.0  # next week total
def test_daily_variability_feature_zero_for_constant_week():
    user = _make_user_with_n_days(14)
    X, y = build_weekly_training_data(user)

    features = X[0]

    assert features["daily_variability"] == 0.0
def test_balance_and_dominance_features_present():
    user = _make_user_with_n_days(14)
    X, y = build_weekly_training_data(user)

    features = X[0]

    assert "category_balance" in features
    assert "dominance_ratio" in features

    assert features["category_balance"] == 1.0
    assert features["dominance_ratio"] == 60.0 / 420.0

def test_category_dominance_ratio_single_category():
    user = _make_user_with_n_days(14)
    X, y = build_weekly_training_data(user)

    features = X[0]

    assert "category_dominance_ratio" in features
    assert features["category_dominance_ratio"] == 1.0
