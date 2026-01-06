"""
Responsibility:
Handles persistence of user activity data.
Converts between JSON storage format and core domain objects.
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Optional

from core.user import User
from core.day_log import DayLog
from core.activity import Activity


class Store:
    """
    Central persistence layer for loading and saving user data.
    """

    def __init__(self, data_dir: Path):
        self.data_dir = data_dir
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def load_user(self, user_id: str) -> Optional[User]:
        """
        Load a user and all associated activity logs from storage.
        """
        file_path = self.data_dir / f"{user_id}.json"

        if not file_path.exists():
            return None

        with file_path.open("r", encoding="utf-8") as f:
            raw = json.load(f)

        user = User(
            user_id=raw["user_id"],
        )

        for log_data in raw.get("logs", []):
            date = datetime.fromisoformat(log_data["date"]).date()
            day_log = DayLog(log_date=date)

            for a in log_data.get("activities", []):
                activity = Activity(
                    name=a["name"],
                    category=a["category"],
                    duration_minutes=a["duration_minutes"],
                    timestamp=datetime.fromisoformat(a["timestamp"]),
                    mood=a.get("mood"),
                )
                day_log.add_activity(activity)

            user.add_activity_log(day_log)

        return user

    def save_user(self, user: User) -> None:
        """
        Persist a user and all activity logs to storage.
        """
        file_path = self.data_dir / f"{user.get_user_id()}.json"

        data = {
            "user_id": user.get_user_id(),
            "logs": [],
        }

        for log in user.get_all_logs():
            log_entry = {
                "date": log.get_date().isoformat(),
                "activities": [],
            }

            for activity in log.get_activities():
                log_entry["activities"].append(
                    {
                        "name": activity.get_name(),
                        "category": activity.get_category(),
                        "duration_minutes": activity.get_duration_minutes(),
                        "timestamp": activity.get_timestamp().isoformat(),
                        "mood": activity.get_mood(),
                    }
                )

            data["logs"].append(log_entry)

        with file_path.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
