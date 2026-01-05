"""
Responsibility:
Defines the User entity that owns and manages activity logs.
"""

from datetime import date
from typing import Dict, List, Optional
from core.activity import Activity
from core.day_log import DayLog


class User:
    """
    Represents a user who owns activity logs across multiple dates.
    """

    def __init__(self, user_id: str):
        if not isinstance(user_id, str) or not user_id.strip():
            raise ValueError("user_id must be a non-empty string.")

        self._user_id = user_id
        self._day_logs: Dict[date, DayLog] = {}

    def log_activity(self, activity: Activity) -> None:
        if not isinstance(activity, Activity):
            raise TypeError("Only Activity instances can be logged.")

        activity_date = activity.get_timestamp().date()

        if activity_date not in self._day_logs:
            self._day_logs[activity_date] = DayLog(activity_date)

        self._day_logs[activity_date].add_activity(activity)

    def get_day_log(self, log_date: date) -> Optional[DayLog]:
        if not isinstance(log_date, date):
            raise TypeError("log_date must be a date instance.")

        return self._day_logs.get(log_date)

    def get_all_logs(self) -> List[DayLog]:
        return list(self._day_logs.values())

    def get_user_id(self) -> str:
        return self._user_id
