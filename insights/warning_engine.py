"""
warning_engine.py

Purpose:
--------
Translate recent risk trajectory states into human-facing warning levels.
This module does NOT detect risk. It does NOT compute features.
It only interprets the *persistence and direction* of already-computed risk states.

Inputs:
-------
- A sequence of recent risk states (e.g. ["R0", "R1", "R2"])
- Number of weeks observed
- Risk confidence metadata

Outputs:
--------
- warning_level: one of {"none", "watch", "caution", "alert"}
- reason: short, factual explanation of why the warning exists
- trajectory: recent risk evolution

Design Constraints:
-------------------
- Must be deterministic and stateless
- Must never inspect raw analytics features
- Must never mutate risk states
- Must never escalate faster than risk
- Must support de-escalation when recovery is observed

Philosophy:
-----------
Risk answers: "What is happening structurally?"
Warning answers: "Is this pattern established enough to surface now?"

A single volatile week is never sufficient for a warning.
Warnings respond to *patterns*, not *peaks*.
"""


def evaluate_warning(risk_history, weeks_observed, confidence):
    """
    Evaluate whether a warning should be raised based on recent risk trajectory.
    """

    # --- Safety guards ---
    if not risk_history or weeks_observed < 2:
        return {
            "warning_level": "none",
            "reason": "Insufficient history for warning evaluation.",
            "trajectory": risk_history,
        }

    # Map risk levels to ordinal values (ordering only, not scoring)
    risk_rank = {"R0": 0, "R1": 1, "R2": 2, "R3": 3}
    ranked = [risk_rank.get(r, 0) for r in risk_history]

    latest = ranked[-1]
    prev = ranked[-2]

    # Count persistence of current risk level
    same_count = 1
    for r in reversed(ranked[:-1]):
        if r == latest:
            same_count += 1
        else:
            break

    # Detect escalation
    escalated = latest > prev

    # --- Warning rules ---

    # Rule 1: Stable or recovered trajectory
    if latest == 0:
        return {
            "warning_level": "none",
            "reason": "Trajectory is stable or recovering.",
            "trajectory": risk_history,
        }

    # Rule 2: First persistence at low risk → WATCH
    if latest == 1 and same_count == 2:
        return {
            "warning_level": "watch",
            "reason": "Early signs of persistent instability.",
            "trajectory": risk_history,
        }

    # Rule 3: ALERT — persistent high risk with sufficient confidence
    if latest >= 2 and same_count >= 2 and confidence != "low":
        return {
            "warning_level": "alert",
            "reason": "Persistent high-risk trajectory detected.",
            "trajectory": risk_history,
        }

    # Rule 4: CAUTION — escalation or long persistence
    if latest >= 1 and (escalated or same_count >= 3):
        return {
            "warning_level": "caution",
            "reason": "Risk escalation or sustained instability detected.",
            "trajectory": risk_history,
        }

    # Default fallback
    return {
        "warning_level": "none",
        "reason": "No actionable warning pattern detected.",
        "trajectory": risk_history,
    }
