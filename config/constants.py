"""
Responsibility:
Defines global constants and allowed values shared across the system.
These represent domain facts, not configurable behavior.
"""

# -----------------------------
# Activity categories
# -----------------------------

WORK = "Work"
STUDY = "Study"
HEALTH = "Health"
LEISURE = "Leisure"

ALL_CATEGORIES = {
    WORK,
    STUDY,
    HEALTH,
    LEISURE,
}


# -----------------------------
# Category → activity mapping
# -----------------------------

CATEGORY_ACTIVITIES = {
    WORK: {"Coding", "Meetings", "Emails"},
    STUDY: {"Reading", "Practice", "Research"},
    HEALTH: {"Workout", "Walking", "Yoga"},
    LEISURE: {"Gaming", "Music", "TV"},
}


# -----------------------------
# Mood scale
# -----------------------------

# Allowed mood values (None means not recorded)
MIN_MOOD = 1
MAX_MOOD = 5
ALLOWED_MOODS = {None, 1, 2, 3, 4, 5}


# -----------------------------
# Time assumptions
# -----------------------------

MINUTES_PER_HOUR = 60
HOURS_PER_DAY = 24
MINUTES_PER_DAY = HOURS_PER_DAY * MINUTES_PER_HOUR
