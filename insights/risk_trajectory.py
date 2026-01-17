# insights/risk_trajectory.py

from typing import List, Dict

RISK_ORDER = {
    "R0": 0,
    "R1": 1,
    "R2": 2,
    "R3": 3,
}


def evaluate_risk_trajectory(risk_history: List[str]) -> Dict:
    """
    Evaluate warning state based on recent risk trajectory.
    Implements Risk Trajectory State Machine (v2).
    """

    # -----------------------------
    # Minimum history requirement
    # -----------------------------
    if len(risk_history) < 3:
        return _none(risk_history)

    recent = risk_history[-3:]

    # -----------------------------
    # R4 uncertainty barrier
    # -----------------------------
    if "R4" in recent:
        return _none(recent)

    w2, w1, w0 = recent

    # -----------------------------
    # Silence rules (trend-based)
    # -----------------------------
    if _is_improving(w1, w0):
        return _none(recent)

    if _is_oscillating(w2, w1, w0):
        return _none(recent)

    # -----------------------------
    # Critical warnings 🔴
    # -----------------------------
    if w1 == "R3" and w0 == "R3":
        return _critical(
            recent,
            "Sustained fragile trajectory across multiple weeks",
        )

    if [w2, w1, w0] == ["R2", "R3", "R3"]:
        return _critical(
            recent,
            "Sustained fragile trajectory across multiple weeks",
        )

    if [w2, w1, w0] == ["R1", "R2", "R3"]:
        return _critical(
            recent,
            "Rapid escalation from moderate risk to fragility",
        )

    # -----------------------------
    # Elevated warnings 🟠
    # -----------------------------
    if w1 == "R2" and w0 == "R2":
        return _elevated(
            recent,
            "Volatility persists without recovery",
        )

    if [w2, w1, w0] == ["R1", "R2", "R2"]:
        return _elevated(
            recent,
            "Volatility persists without recovery",
        )

    if w1 == "R2" and w0 == "R3":
        return _elevated(
            recent,
            "Transition from volatility to fragile trajectory",
        )

    # -----------------------------
    # Early warnings 🟡
    # -----------------------------
    if [w2, w1, w0] == ["R0", "R1", "R1"]:
        return _early(
            recent,
            "Risk emerging across consecutive weeks",
        )

    if w1 == "R1" and w0 == "R2":
        return _early(
            recent,
            "Upward drift toward volatility",
        )

    if w1 == "R2" and w0 == "R2":
        return _early(
            recent,
            "Sustained moderate risk",
        )

    # -----------------------------
    # Final silence rule ⚪
    # (only if no trajectory pattern matched)
    # -----------------------------
    if max(RISK_ORDER[w] for w in recent) <= RISK_ORDER["R1"]:
        return _none(recent)

    return _none(recent)


# ==========================================================
# Helper rules
# ==========================================================

def _is_improving(prev: str, curr: str) -> bool:
    return RISK_ORDER[curr] < RISK_ORDER[prev]


def _is_oscillating(w2: str, w1: str, w0: str) -> bool:
    return w2 == w0 and RISK_ORDER[w1] < RISK_ORDER[w0]


# ==========================================================
# Output helpers
# ==========================================================

def _none(traj: List[str]) -> Dict:
    return {
        "warning_level": "none",
        "reason": None,
        "trajectory": traj,
        "weeks_observed": len(traj),
    }


def _early(traj: List[str], reason: str) -> Dict:
    return {
        "warning_level": "early",
        "reason": reason,
        "trajectory": traj,
        "weeks_observed": len(traj),
    }


def _elevated(traj: List[str], reason: str) -> Dict:
    return {
        "warning_level": "elevated",
        "reason": reason,
        "trajectory": traj,
        "weeks_observed": len(traj),
    }


def _critical(traj: List[str], reason: str) -> Dict:
    return {
        "warning_level": "critical",
        "reason": reason,
        "trajectory": traj,
        "weeks_observed": len(traj),
    }
