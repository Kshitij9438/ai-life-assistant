"""
Responsibility:
Tests analytics computations and aggregations.
"""
from analytics.aggregations import (
    total_duration_per_day,
    daily_category_minutes,
    total_duration_per_category
)
from analytics.statistics import (daily_average, activity_variability, category_share, category_balance,dominance_ratio)
def test_total_duration_per_day():
    logs = [
        {
            "date": "2024-06-01",
            "activities": [
                {"category": "Work", "duration_minutes": 120},
                {"category": "Study", "duration_minutes": 60},
            ],
        },
        {
            "date": "2024-06-02",
            "activities": [
                {"category": "Exercise", "duration_minutes": 30},
                {"category": "Work", "duration_minutes": 90},
            ],
        },
    ]

    expected = {
        "2024-06-01": 180,
        "2024-06-02": 120,
    }

    assert total_duration_per_day(logs) == expected

def test_daily_category_minutes():
    logs = [
        {
            "date": "2024-06-01",
            "activities": [
                {"category": "Work", "duration_minutes": 120},
                {"category": "Study", "duration_minutes": 60},
                {"category": "Work", "duration_minutes": 30},
            ],
        },
        {
            "date": "2024-06-02",
            "activities": [
                {"category": "Exercise", "duration_minutes": 30},
                {"category": "Work", "duration_minutes": 90},
            ],
        },
    ]

    expected = {
        "2024-06-01": {
            "Work": 150,
            "Study": 60,
        },
        "2024-06-02": {
            "Exercise": 30,
            "Work": 90,
        },
    }

    assert daily_category_minutes(logs) == expected
def test_total_duration_per_category():
    logs = [
        {
            "date": "2024-06-01",
            "activities": [
                {"category": "Work", "duration_minutes": 120},
                {"category": "Study", "duration_minutes": 60},
            ],
        },
        {
            "date": "2024-06-02",
            "activities": [
                {"category": "Exercise", "duration_minutes": 30},
                {"category": "Work", "duration_minutes": 90},
            ],
        },
    ]

    expected = {
        "Work": 210,
        "Study": 60,
        "Exercise": 30,
    }

    assert total_duration_per_category(logs) == expected
def test_daily_average():
    daily_minutes = {
        "2024-06-01": 180,
        "2024-06-02": 120,
        "2024-06-03": 150,
    }

    avg = daily_average(daily_minutes)
    assert avg == 150.0
def test_activity_variability_non_zero():
    daily_minutes = {
        "2024-06-01": 180,
        "2024-06-02": 120,
        "2024-06-03": 150,
    }

    variability = activity_variability(daily_minutes)
    assert round(variability, 2) == 24.49


def test_activity_variability_zero():
    daily_minutes = {
        "2024-06-01": 100,
        "2024-06-02": 100,
        "2024-06-03": 100,
    }

    variability = activity_variability(daily_minutes)
    assert variability == 0.0
def test_category_share():
    category_minutes = {
        "Work": 210,
        "Study": 60,
        "Exercise": 30,
    }

    shares = category_share(category_minutes)

    expected = {
        "Work": 0.7,
        "Study": 0.2,
        "Exercise": 0.1,
    }

    for category in expected.keys():
        assert round(shares[category], 2) == expected[category]
def test_category_balance():
    balanced = {
        "Work": 100,
        "Study": 100,
        "Health": 100,
    }

    skewed = {
        "Work": 280,
        "Leisure": 20,
    }

    assert round(category_balance(balanced), 2) == 1.0
    assert round(category_balance(skewed), 2) < 0.5
def test_dominance_ratio():
    balanced = {
        "Work": 100,
        "Study": 100,
        "Health": 100,
    }

    skewed = {
        "Work": 280,
        "Leisure": 20,
    }

    assert round(dominance_ratio(balanced), 2) == 0.33
    assert round(dominance_ratio(skewed), 2) == 0.93
