from datetime import datetime
from typing import Dict, Tuple, Optional


def split_into_weeks(
    daily_totals: Dict[str, int],
) -> Tuple[Dict[str, int], Optional[Dict[str, int]]]:
    """
    Splits daily totals into current and previous week (rolling windows).
    """
    if not daily_totals:
        return {}, None

    # Convert and sort dates
    parsed_dates = sorted(
        datetime.strptime(d, "%Y-%m-%d").date()
        for d in daily_totals.keys()
    )

    # Take rolling windows from available data
    current_week_dates = parsed_dates[-7:]
    previous_week_dates = parsed_dates[-14:-7]

    current_week = {
        d.strftime("%Y-%m-%d"): daily_totals[d.strftime("%Y-%m-%d")]
        for d in current_week_dates
    }

    previous_week = {
        d.strftime("%Y-%m-%d"): daily_totals[d.strftime("%Y-%m-%d")]
        for d in previous_week_dates
    }

    return current_week, previous_week if previous_week else None
