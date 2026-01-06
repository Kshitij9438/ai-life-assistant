"""
Responsibility:
Defines canonical filesystem paths used across the system.
All paths are relative to the project root.
"""

from pathlib import Path


# Project root (assumes this file is config/paths.py)
PROJECT_ROOT = Path(__file__).resolve().parents[1]


# -----------------------------
# Data paths
# -----------------------------
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
SYNTHETIC_DATA_DIR = DATA_DIR / "synthetic"


# -----------------------------
# Reports & outputs
# -----------------------------
REPORTS_DIR = PROJECT_ROOT / "reports"
DAILY_REPORTS_DIR = REPORTS_DIR / "daily"
WEEKLY_REPORTS_DIR = REPORTS_DIR / "weekly"
FIGURES_DIR = REPORTS_DIR / "figures"


# -----------------------------
# Models & artifacts (future)
# -----------------------------
MODELS_DIR = PROJECT_ROOT / "models"
