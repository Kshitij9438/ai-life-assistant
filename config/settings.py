"""
Responsibility:
Defines system-wide configuration values that control behavior.
These are tunable parameters, not logic.
"""

# -----------------------------
# Analytics settings
# -----------------------------

# Minimum minutes to consider a day as "active"
MIN_ACTIVE_MINUTES_PER_DAY = 30

# Number of days required to compute weekly trends
DAYS_PER_WEEK = 7


# -----------------------------
# Insight thresholds
# -----------------------------

# If one category exceeds this share of total time, it is considered dominant
DOMINANT_CATEGORY_SHARE = 0.6

# Below this share, a category is considered underrepresented
UNDERREPRESENTED_CATEGORY_SHARE = 0.15


# -----------------------------
# Recommendation rules
# -----------------------------

# Minimum days of data required to generate recommendations
MIN_DAYS_FOR_RECOMMENDATIONS = 5


# -----------------------------
# Machine Learning settings
# -----------------------------

# Minimum samples required to train a model
MIN_SAMPLES_FOR_TRAINING = 7

# Train/test split ratio
TRAIN_SPLIT_RATIO = 0.8

# Random seed for reproducibility (if used later)
RANDOM_SEED = 42


# -----------------------------
# Reporting
# -----------------------------

# Default number of days to include in rolling summaries
ROLLING_WINDOW_DAYS = 7
