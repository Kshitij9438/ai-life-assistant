# -----------------------------
# Risk thresholds (v1.1)
# -----------------------------

DAILY_VARIABILITY_HIGH = 90.0     # minutes (raw scale)
DOMINANCE_RATIO_HIGH  = 0.65
CATEGORY_BALANCE_LOW  = 0.35


def _get_feature(features: dict, *keys: str, default: float = 0.0) -> float:
    """
    Helper to support multiple feature aliases.
    """
    for k in keys:
        if k in features:
            return features[k]
    return default


def classify_weekly_risk(features: dict[str, float]) -> dict:
    """
    Classify structural trajectory risk based on weekly features.

    Returns:
        {
            "risk_level": "R0" | "R1" | "R2" | "R3" | "R4",
            "risk_label": str,
            "drivers": list[str]
        }
    """

    if not features:
        return {
            "risk_level": "R4",
            "risk_label": "insufficient_signal",
            "drivers": [],
        }

    dv = _get_feature(features, "daily_variability", "dv")
    dr = _get_feature(features, "dominance_ratio", "dr")
    cb = _get_feature(features, "category_balance", "cb")

    drivers: list[str] = []

    # -----------------------------
    # Variability scale handling
    # -----------------------------
    if dv <= 1.0:
        # normalized variability
        is_high_variability = dv >= 0.7
    else:
        # raw variability (minutes)
        is_high_variability = dv >= DAILY_VARIABILITY_HIGH

    is_high_dominance = dr >= DOMINANCE_RATIO_HIGH
    is_low_balance    = cb <= CATEGORY_BALANCE_LOW

    if is_high_variability:
        drivers.append("high_variability")
    if is_high_dominance:
        drivers.append("high_dominance")
    if is_low_balance:
        drivers.append("low_balance")

    # -----------------------------
    # Risk level resolution (ordered)
    # -----------------------------

    if is_high_variability and is_high_dominance:
        return {
            "risk_level": "R3",
            "risk_label": "fragile_trajectory",
            "drivers": drivers,
        }

    if is_high_variability:
        return {
            "risk_level": "R2",
            "risk_label": "volatility_risk",
            "drivers": drivers,
        }

    if is_high_dominance or is_low_balance:
        return {
            "risk_level": "R1",
            "risk_label": "load_concentration_risk",
            "drivers": drivers,
        }

    return {
        "risk_level": "R0",
        "risk_label": "stable_trajectory",
        "drivers": [],
    }


def detect_risk_transition(prev: dict | None, curr: dict | None) -> str:
    """
    Detect directional risk movement.
    """
    if not prev or not curr:
        return "unknown"

    prev_lvl = prev.get("risk_level")
    curr_lvl = curr.get("risk_level")

    if prev_lvl is None or curr_lvl is None:
        return "unknown"

    if curr_lvl > prev_lvl:
        return "increasing_risk"
    if curr_lvl < prev_lvl:
        return "decreasing_risk"

    return "stable"
