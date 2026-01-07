from typing import List


def mean_absolute_error(y_true: List[float], y_pred: List[float]) -> float:
    if not y_true:
        return 0.0

    return sum(abs(t - p) for t, p in zip(y_true, y_pred)) / len(y_true)
