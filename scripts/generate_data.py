"""
Responsibility:
Generates synthetic activity data for development and testing.
"""

import random
from datetime import datetime, timedelta

from core.activity import Activity
from core.user import User
import json
from pathlib import Path

def _clamp(value: int, min_val: int, max_val: int) -> int:
    return max(min_val, min(value, max_val))

RANDOM_SEED = None  # set to an int (e.g. 42) for reproducibility

if RANDOM_SEED is not None:
    random.seed(RANDOM_SEED)

CATEGORIES = {
    "Work": ["Coding", "Meetings", "Emails"],
    "Study": ["Reading", "Practice", "Research"],
    "Health": ["Workout", "Walking", "Yoga"],
    "Leisure": ["Gaming", "Music", "TV"],
}


def generate_random_activity(base_date: datetime) -> Activity:
    category = random.choice(list(CATEGORIES.keys()))
    name = random.choice(CATEGORIES[category])

    hour = random.randint(6, 22)
    minute = random.choice([0, 15, 30, 45])

    timestamp = base_date.replace(
        hour=hour,
        minute=minute,
        second=0,
        microsecond=0,
    )

    duration_minutes = random.choice([30, 45, 60, 90, 120])

    mood = random.choice([None, 2, 3, 4, 5])

    return Activity(
        name=name,
        category=category,
        duration_minutes=duration_minutes,
        timestamp=timestamp,
        mood=mood,
    )


def generate_user_with_activity(days: int) -> User:
    if not isinstance(days, int) or days <= 0:
        raise ValueError("days must be a positive integer.")

    user = User(user_id="synthetic_user")

    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

    # --- Temporal state ---
    prev_total_minutes = random.randint(240, 480)  # 4–8 hours baseline
    dominant_category = random.choice(list(CATEGORIES.keys()))
    start_date = today - timedelta(days=days - 1)
    for i in range(days):
        base_date = start_date + timedelta(days=i)


        # Weekly rhythm: weekdays busier than weekends
        is_weekend = base_date.weekday() >= 5
        base_minutes = prev_total_minutes * (0.85 if is_weekend else 1.05)

        # Small random drift
        target_minutes = int(base_minutes + random.randint(-60, 60))
        target_minutes = _clamp(target_minutes, 180, 600)

        activities = []
        remaining_minutes = target_minutes

        activity_count = random.randint(3, 6)

        for _ in range(activity_count):
            if remaining_minutes <= 0:
                break

            # Category inertia
            category = (
                dominant_category
                if random.random() < 0.6
                else random.choice(list(CATEGORIES.keys()))
            )

            name = random.choice(CATEGORIES[category])

            duration = min(
                random.choice([30, 45, 60, 90]),
                remaining_minutes,
            )

            hour = random.randint(6, 22)
            minute = random.choice([0, 15, 30, 45])

            timestamp = base_date.replace(
                hour=hour,
                minute=minute,
                second=0,
                microsecond=0,
            )

            mood = random.choice([None, 3, 4, 5])

            activity = Activity(
                name=name,
                category=category,
                duration_minutes=duration,
                timestamp=timestamp,
                mood=mood,
            )

            user.log_activity(activity)
            activities.append(activity)

            remaining_minutes -= duration

        # Update temporal state for next day
        prev_total_minutes = target_minutes
        dominant_category = max(
            (a.get_category() for a in activities),
            key=lambda c: sum(
                a.get_duration_minutes()
                for a in activities
                if a.get_category() == c
            ),
            default=dominant_category,
        )

    return user

def serialize_user(user: User) -> dict:
    return {
        "user_id": user.get_user_id(),
        "logs": [
            {
                "date": log.get_date().isoformat(),
                "activities": [
                    {
                        "name": activity.get_name(),
                        "category": activity.get_category(),
                        "duration_minutes": activity.get_duration_minutes(),
                        "timestamp": activity.get_timestamp().isoformat(),
                        "mood": activity.get_mood(),
                    }
                    for activity in log.get_activities()
                ],
            }
            for log in user.get_all_logs()
        ],
    }


def save_user_to_json(user: User, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)

    data = serialize_user(user)
    file_path = output_dir / f"{user.get_user_id()}.json"

    with file_path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
if __name__ == "__main__":
    user = generate_user_with_activity(days=14)
    save_user_to_json(user, Path("data/synthetic"))
