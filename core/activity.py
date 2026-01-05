"""
Responsibility:
Defines the Activity entity representing a single logged action.
"""

from datetime import datetime


class Activity:
    """
    Represents a single, atomic activity performed by a user.
    """

    def __init__(
        self,
        name: str,
        category: str,
        duration_minutes: int,
        timestamp: datetime,
        mood: int | None = None,
    ):
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Activity name must be a non-empty string.")

        if not isinstance(category, str) or not category.strip():
            raise ValueError("Activity category must be a non-empty string.")

        if not isinstance(duration_minutes, int) or duration_minutes <= 0:
            raise ValueError("Activity duration must be a positive integer.")

        if not isinstance(timestamp, datetime):
            raise TypeError("timestamp must be a datetime instance.")

        if mood is not None:
            if not isinstance(mood, int) or not (1 <= mood <= 5):
                raise ValueError("Mood must be an integer between 1 and 5.")

        self._name = name
        self._category = category
        self._duration_minutes = duration_minutes
        self._timestamp = timestamp
        self._mood = mood

    def get_name(self) -> str:
        return self._name

    def get_category(self) -> str:
        return self._category

    def get_duration_minutes(self) -> int:
        return self._duration_minutes

    def get_timestamp(self) -> datetime:
        return self._timestamp

    def get_mood(self) -> int | None:
        return self._mood
