"""
Responsibility:
Runs the full end-to-end weekly intelligence pipeline (v2: early warning).
"""

from pipelines.ingest import ingest_user
from pipelines.analyze import analyze_user
from pipelines.week_utils import split_into_weeks

from ml.train import build_weekly_training_data
from ml.train_weekly_model import train_weekly_model
from ml.evaluate_weekly_model import evaluate_weekly_baseline
from ml.metrics import mean_absolute_error

from insights.explainations import explain_weekly_prediction
from insights.risk import classify_weekly_risk
from insights.risk_trajectory import evaluate_risk_trajectory


def run_weekly_intelligence_v2(
    user_id: str,
    *,
    risk_history: list[str] | None = None,
) -> dict:
    """
    Run full weekly intelligence pipeline for a user (v2).

    Adds:
    - Risk trajectory evaluation
    - Early warning intelligence

    Backward-compatible with v1.
    """

    # --------------------
    # 1️⃣ Ingest
    # --------------------
    user = ingest_user(user_id)
    if not user:
        return {
            "status": {
                "state": "error",
                "message": f"No data found for user '{user_id}'.",
            }
        }

    # --------------------
    # 2️⃣ Analytics
    # --------------------
    analysis = analyze_user(user)
    daily_totals = analysis["daily_totals"]

    current_week, previous_week = split_into_weeks(daily_totals)

    if not current_week or not previous_week:
        return {
            "status": {
                "state": "insufficient_data",
                "message": "At least two full weeks of data are required.",
            }
        }

    previous_week_total = sum(previous_week.values())

    # --------------------
    # 3️⃣ Baseline Evaluation
    # --------------------
    y_true_base, y_pred_base = evaluate_weekly_baseline(user)
    baseline_mae = mean_absolute_error(y_true_base, y_pred_base)

    # --------------------
    # 4️⃣ Model Training (doctrine-aware)
    # --------------------
    prediction = previous_week_total
    model_mae = None
    ml_used = False
    coefficients = {}

    try:
        X, y_true_model = build_weekly_training_data(user)
        model, coefficients = train_weekly_model(user)
        prediction = model.predict(X)[0]
        model_mae = mean_absolute_error(y_true_model, [prediction])
        ml_used = True

    except ValueError:
        # Correct behavior: baseline-only intelligence
        prediction = previous_week_total
        model_mae = None
        ml_used = False

    # --------------------
    # 5️⃣ Explanation
    # --------------------
    features = X[0]

    explanation = explain_weekly_prediction(
        features=features,
        coefficients=coefficients if ml_used else {},
        baseline_value=previous_week_total,
        previous_week_value=previous_week_total,
        prediction=prediction,
        enforce_conservation=False,
    )

    # --------------------
    # 6️⃣ Risk Classification (v1)
    # --------------------
    current_risk = classify_weekly_risk(features)

    # --------------------
    # 7️⃣ Risk Trajectory & Warning (v2)
    # --------------------
    if risk_history is None:
        # No history → silence
        warning = {
            "warning_level": "none",
            "reason": None,
            "trajectory": [current_risk["risk_level"]],
            "weeks_observed": 1,
        }
    else:
        full_history = risk_history + [current_risk["risk_level"]]
        warning = evaluate_risk_trajectory(full_history)

    # --------------------
    # 8️⃣ Final Output Contract
    # --------------------
    return {
        "status": {
            "state": "ok",
            "message": "Weekly intelligence generated successfully.",
        },

        "prediction": {
            "next_week_minutes": prediction,
            "previous_week_minutes": previous_week_total,
            "baseline_prediction": previous_week_total,
            "delta_vs_previous": prediction - previous_week_total,
            "delta_vs_baseline": prediction - previous_week_total,
        },

        "explanation": explanation,

        "evaluation": {
            "baseline_mae": baseline_mae,
            "model_mae": model_mae,
            "beats_baseline": (
                model_mae < baseline_mae if model_mae is not None else False
            ),
            "ml_used": ml_used,
            "samples_used": len(X) if ml_used else 0,
        },

        "context": {
            "weeks_used": 2,
            "features_used": list(features.keys()),
            "daily_variability": features.get("daily_variability", 0.0),
            "category_balance": features.get("category_balance", 0.0),
            "dominance_ratio": features.get("dominance_ratio", 0.0),
        },

        "risk": {
            **current_risk,
            "confidence": explanation["confidence_hint"],
        },

        "warning": warning,

        "meta": {
            "model_type": "LinearRegression" if ml_used else None,
            "explainability": "additive",
            "baseline_type": "previous_week",
            "ml_status": "active" if ml_used else "refused_insufficient_data",
            "version": "v2.0",
        },
    }
