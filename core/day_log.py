"""
Responsibility:
Represents a collection of activities associated with a single date.
"""

from datetime import date
from typing import List
from core.activity import Activity


class DayLog:
    """
    Groups all activities that occur on a single calendar date.
    """

    def __init__(self, log_date: date):
        if not isinstance(log_date, date):
            raise TypeError("log_date must be a date instance.")

        self._date = log_date
        self._activities: List[Activity] = []

    def add_activity(self, activity: Activity) -> None:
        if not isinstance(activity, Activity):
            raise TypeError("Only Activity instances can be added.")

        activity_date = activity.get_timestamp().date()
        if activity_date != self._date:
            raise ValueError(
                f"Activity date {activity_date} does not match DayLog date {self._date}."
            )

        self._activities.append(activity)
        self._activities.sort(key=lambda a: a.get_timestamp())

    def get_activities(self) -> List[Activity]:
        return list(self._activities)

    def total_duration(self) -> int:
        return sum(a.get_duration_minutes() for a in self._activities)

    def get_date(self) -> date:
        return self._date
