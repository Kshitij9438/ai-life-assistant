"""
Responsibility:
Tests correctness of core domain entities.
"""
from datetime import datetime, date

import pytest

from core.activity import Activity
from core.day_log import DayLog
from core.user import User


# -------------------------
# Activity invariants
# -------------------------

def test_activity_valid_creation():
    activity = Activity(
        name="Coding",
        category="Work",
        duration_minutes=60,
        timestamp=datetime(2026, 1, 6, 10, 0),
        mood=4,
    )
    assert activity.get_name() == "Coding"
    assert activity.get_duration_minutes() == 60


def test_activity_invalid_duration():
    with pytest.raises(ValueError):
        Activity(
            name="Coding",
            category="Work",
            duration_minutes=0,
            timestamp=datetime.now(),
        )


def test_activity_invalid_mood():
    with pytest.raises(ValueError):
        Activity(
            name="Coding",
            category="Work",
            duration_minutes=30,
            timestamp=datetime.now(),
            mood=10,
        )


# -------------------------
# DayLog invariants
# -------------------------

def test_daylog_accepts_only_matching_date_activity():
    log_date = date(2026, 1, 6)
    day_log = DayLog(log_date)

    valid_activity = Activity(
        name="Reading",
        category="Study",
        duration_minutes=45,
        timestamp=datetime(2026, 1, 6, 9, 0),
    )

    day_log.add_activity(valid_activity)
    assert len(day_log.get_activities()) == 1


def test_daylog_rejects_foreign_date_activity():
    log_date = date(2026, 1, 6)
    day_log = DayLog(log_date)

    invalid_activity = Activity(
        name="Workout",
        category="Health",
        duration_minutes=30,
        timestamp=datetime(2026, 1, 7, 7, 0),
    )

    with pytest.raises(ValueError):
        day_log.add_activity(invalid_activity)


def test_daylog_returns_copy_of_activities():
    log_date = date(2026, 1, 6)
    day_log = DayLog(log_date)

    activity = Activity(
        name="Coding",
        category="Work",
        duration_minutes=60,
        timestamp=datetime(2026, 1, 6, 11, 0),
    )

    day_log.add_activity(activity)
    activities = day_log.get_activities()
    activities.clear()

    assert len(day_log.get_activities()) == 1


# -------------------------
# User invariants
# -------------------------

def test_user_creates_single_daylog_per_date():
    user = User("user_1")

    activity1 = Activity(
        name="Coding",
        category="Work",
        duration_minutes=60,
        timestamp=datetime(2026, 1, 6, 10, 0),
    )

    activity2 = Activity(
        name="Reading",
        category="Study",
        duration_minutes=30,
        timestamp=datetime(2026, 1, 6, 15, 0),
    )

    user.log_activity(activity1)
    user.log_activity(activity2)

    logs = user.get_all_logs()
    assert len(logs) == 1
    assert logs[0].total_duration() == 90


def test_user_routes_activity_to_correct_daylog():
    user = User("user_2")

    activity = Activity(
        name="Workout",
        category="Health",
        duration_minutes=40,
        timestamp=datetime(2026, 1, 7, 6, 30),
    )

    user.log_activity(activity)
    day_log = user.get_day_log(date(2026, 1, 7))

    assert day_log is not None
    assert day_log.total_duration() == 40
