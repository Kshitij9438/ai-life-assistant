from datetime import datetime
from typing import List, Tuple


def evaluate_weekly_baseline(user) -> Tuple[List[float], List[float]]:
    """
    Returns:
        y_true: list of actual weekly totals
        y_pred: list of baseline predictions (previous week totals)
    """

    if user is None:
        return [], []

    # ---- Build daily totals ----
    daily_totals = {
        log.get_date().isoformat(): log.total_duration()
        for log in user.get_all_logs()
    }

    if len(daily_totals) < 14:
        return [], []

    # ---- Sort dates ----
    sorted_dates = sorted(
        datetime.strptime(d, "%Y-%m-%d").date()
        for d in daily_totals.keys()
    )

    # ---- Build weekly totals (non-overlapping, full weeks only) ----
    weekly_totals: List[float] = []

    while len(sorted_dates) >= 7:
        week_dates = sorted_dates[:7]
        week_total = sum(
            daily_totals[d.strftime("%Y-%m-%d")]
            for d in week_dates
        )
        weekly_totals.append(float(week_total))
        sorted_dates = sorted_dates[7:]

    if len(weekly_totals) < 2:
        return [], []

    # ---- Baseline prediction ----
    y_true: List[float] = []
    y_pred: List[float] = []

    for i in range(len(weekly_totals) - 1):
        y_pred.append(weekly_totals[i])
        y_true.append(weekly_totals[i + 1])

    return y_true, y_pred
