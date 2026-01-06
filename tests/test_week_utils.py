"""
Responsibility:
Tests week-based rolling window utilities.
"""

from pipelines.week_utils import split_into_weeks


def test_split_into_weeks_two_full_weeks():
    daily_totals = {
        "2024-06-01": 30,
        "2024-06-02": 45,
        "2024-06-03": 20,
        "2024-06-04": 50,
        "2024-06-05": 60,
        "2024-06-06": 40,
        "2024-06-07": 70,
        "2024-06-08": 80,
        "2024-06-09": 90,
        "2024-06-10": 100,
        "2024-06-11": 110,
        "2024-06-12": 120,
        "2024-06-13": 130,
        "2024-06-14": 140,
    }

    current_week, previous_week = split_into_weeks(daily_totals)

    assert set(current_week.keys()) == {
        "2024-06-08",
        "2024-06-09",
        "2024-06-10",
        "2024-06-11",
        "2024-06-12",
        "2024-06-13",
        "2024-06-14",
    }

    assert set(previous_week.keys()) == {
        "2024-06-01",
        "2024-06-02",
        "2024-06-03",
        "2024-06-04",
        "2024-06-05",
        "2024-06-06",
        "2024-06-07",
    }


def test_split_into_weeks_less_than_seven_days():
    daily_totals = {
        "2024-06-01": 30,
        "2024-06-02": 45,
        "2024-06-03": 20,
    }

    current_week, previous_week = split_into_weeks(daily_totals)

    assert current_week == daily_totals
    assert previous_week is None


def test_split_into_weeks_exactly_seven_days():
    daily_totals = {
        "2024-06-01": 10,
        "2024-06-02": 20,
        "2024-06-03": 30,
        "2024-06-04": 40,
        "2024-06-05": 50,
        "2024-06-06": 60,
        "2024-06-07": 70,
    }

    current_week, previous_week = split_into_weeks(daily_totals)

    assert current_week == daily_totals
    assert previous_week is None


def test_split_into_weeks_empty_input():
    current_week, previous_week = split_into_weeks({})

    assert current_week == {}
    assert previous_week is None
