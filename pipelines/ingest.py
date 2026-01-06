"""
Responsibility:
Handles ingestion of user activity data into core domain objects.
"""

from typing import Optional

from core.store import Store
from core.user import User
from config.paths import SYNTHETIC_DATA_DIR


def ingest_user(user_id: str) -> Optional[User]:
    """
    Load a user's activity data from storage and return a User object.

    Args:
        user_id: Identifier of the user to ingest.

    Returns:
        User instance if data exists, otherwise None.
    """
    store = Store(SYNTHETIC_DATA_DIR)
    return store.load_user(user_id)
