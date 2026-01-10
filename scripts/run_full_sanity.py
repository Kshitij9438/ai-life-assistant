"""
Runs a complete end-to-end sanity check of the AI Life Assistant system.

Covers:
- Data ingestion
- Analytics
- Feature engineering
- Weekly baseline evaluation
- Weekly ML model training
- Model vs baseline comparison
"""

from pipelines.ingest import ingest_user
from pipelines.analyze import analyze_user

from ml.evaluate_weekly_model import evaluate_weekly_baseline
from ml.train_weekly_model import train_weekly_model
from ml.train import build_weekly_training_data
from ml.metrics import mean_absolute_error

def run_full_sanity(user_id: str) -> None:
    print("\n==============================")
    print("🧪 FULL SYSTEM SANITY CHECK")
    print("==============================\n")

    # 1️⃣ Ingest
    user = ingest_user(user_id)
    if user is None:
        print("❌ User not found")
        return

    print(f"✅ User loaded: {user.get_user_id()}")
    print(f"📅 Total days logged: {len(user.get_all_logs())}\n")

    # 2️⃣ Analytics
    analytics = analyze_user(user)
    print("✅ Analytics computed")
    print(f"   Daily totals: {len(analytics['daily_totals'])} days\n")

    # 3️⃣ Baseline evaluation
    y_true_base, y_pred_base = evaluate_weekly_baseline(user)

    if len(y_true_base) < 1:
        print("⚠️ Not enough data for weekly evaluation (< 2 weeks)")
        return

    baseline_mae = mean_absolute_error(y_true_base, y_pred_base)

    print("📉 Baseline Evaluation")
    print(f"   Samples: {len(y_true_base)}")
    print(f"   MAE: {baseline_mae:.2f}\n")

    # 4️⃣ Model training data
    X, y_true_model = build_weekly_training_data(user)

    print("🧠 ML Training Data")
    print(f"   Samples: {len(X)}")
    if X:
        print(f"   Features per sample: {len(X[0])}\n")
    else:
        print("   Features per sample: N/A\n")

    # 5️⃣ Train model (doctrine-aware)
    try:
        model, coeffs = train_weekly_model(user)
        y_pred_model = model.predict(X)
        model_mae = mean_absolute_error(y_true_model, y_pred_model)

        print("📈 Model Evaluation")
        print(f"   MAE: {model_mae:.2f}\n")

        print("🔍 Model Coefficients (by importance)")
        for k, v in sorted(coeffs.items(), key=lambda x: abs(x[1]), reverse=True):
            print(f"   {k:25s} → {v:.3f}")

        if model_mae < baseline_mae:
            print("\n🏆 Model beats baseline ✔")
        else:
            print("\n⚠️ Model does NOT beat baseline")

    except ValueError as e:
        print("⚠️ Weekly ML skipped (correct behavior)")
        print(f"   Reason: {e}")
        print("   Baseline-only intelligence is active ✔")



if __name__ == "__main__":
    run_full_sanity("synthetic_user")
