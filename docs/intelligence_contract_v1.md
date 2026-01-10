# AI Life Assistant — Weekly Intelligence Contract (v1)

## Purpose

The purpose of this system is **not** to optimize productivity, maximize output, or prescribe lifestyle changes.

The purpose of this system is:

> **To detect, explain, and forecast the sustainability and risk of a user’s activity patterns early enough that meaningful intervention is still possible.**

This is a **decision-support intelligence system**, not a tracking or recommendation engine.

---

## Scope of Intelligence (v1)

In version 1, the system operates **only at weekly resolution** and answers **one class of questions**:

> *“Given recent behavior, is the current trajectory stable, fragile, or at risk — and why?”*

The system explicitly does **not** attempt to:

* optimize behavior
* motivate users
* provide prescriptive schedules
* forecast long-term outcomes
* infer intent or goals

---

## Input Contract

### Required Data

* Daily activity logs with:

  * date
  * duration
  * category (optional but improves fidelity)

### Minimum Data Requirement

* **At least two full weeks of data**
* If this requirement is not met, the system must return:

  * `state: insufficient_data`
  * No prediction
  * No explanation

This is a **hard constraint**.

---

## Core Outputs (Guaranteed)

When sufficient data exists, the system produces a **Weekly Intelligence Report** with the following guaranteed components.

---

## 1️⃣ Prediction Contract

The system produces a **short-horizon forecast only**.

### Output

```json
"prediction": {
  "next_week_minutes": float,
  "previous_week_minutes": float,
  "baseline_prediction": float,
  "delta_vs_previous": float,
  "delta_vs_baseline": float
}
```

### Guarantees

* The baseline prediction is **always** the previous week’s actual value
* No forecast beyond one week is permitted
* Prediction uncertainty is implicitly handled via confidence signals (see below)

---

## 2️⃣ Baseline Awareness Contract

Every model prediction is evaluated **relative to a baseline**.

### Guarantees

* A baseline MAE is always computed
* A model MAE is always computed
* The system must explicitly state whether it beats the baseline

```json
"evaluation": {
  "baseline_mae": float,
  "model_mae": float,
  "beats_baseline": boolean,
  "samples_used": int
}
```

### Principle

> **If the model does not outperform the baseline, its prediction must not be treated as authoritative.**

This prevents overconfidence.

---

## 3️⃣ Explanation Intelligence Contract

Every prediction is accompanied by a **fully numeric, additive explanation**.

### Explanation Properties

* Each feature contributes a signed numeric value
* Top positive and negative drivers are surfaced
* The explanation is machine-verifiable
* Optional conservation enforcement ensures faithfulness when required

```json
"explanation": {
  "prediction": float,
  "baseline": float,
  "previous_week": float,

  "delta_vs_baseline": float,
  "delta_vs_previous": float,

  "feature_contributions": {
    "<feature_name>": float
  },

  "top_positive_drivers": [
    [feature_name, contribution]
  ],

  "top_negative_drivers": [
    [feature_name, contribution]
  ],

  "confidence_hint": "stable" | "moderate" | "fragile",
  "total_contribution": float
}
```

### Explanation Rule

> **Explanations must describe *structural causes*, not behavioral judgments.**

---

## 4️⃣ Stability & Risk Signaling Contract

The system must provide an explicit **confidence hint**, derived from observed structure:

* Variability
* Dominance concentration
* Balance dispersion

### Allowed Values

* `"stable"` → low variance, low dominance
* `"moderate"` → mixed signals
* `"fragile"` → high dominance or instability

### Principle

> **Confidence describes trajectory reliability, not correctness.**

---

## 5️⃣ Context Contract

The system exposes *why* it reached its conclusion by surfacing relevant context.

```json
"context": {
  "weeks_used": int,
  "features_used": [string],
  "daily_variability": float,
  "category_balance": float,
  "dominance_ratio": float
}
```

This allows:

* auditability
* future visualization
* external interpretation

---

## 6️⃣ Refusal & Silence Contract

The system must **refuse** to produce intelligence when:

* fewer than two weeks of data exist
* signal quality is insufficient
* confidence cannot be reasonably assessed

In such cases, the system returns:

```json
"status": {
  "state": "insufficient_data",
  "message": "At least two full weeks of data are required."
}
```

Silence is considered a **correct output**.

---

## 7️⃣ Non-Goals (Explicit)

Version 1 does **not**:

* prescribe actions
* give advice
* label behavior as good or bad
* predict burnout, motivation, or success
* operate beyond weekly timescales

These are **deliberate exclusions**.

---

## Intelligence Philosophy (Non-Negotiable)

1. **Baseline humility over predictive confidence**
2. **Explanation before persuasion**
3. **Stability detection over optimization**
4. **Refusal is a valid form of intelligence**
5. **Short-horizon trust beats long-horizon speculation**

---

## Completion Criteria for v1

Version 1 is considered **complete** when:

* The weekly intelligence pipeline runs end-to-end
* Predictions are baseline-aware
* Explanations are additive and testable
* Stability classification is consistent
* The system knows when *not* to speak

No additional features are required for v1.

---

## Closing Statement

This system does not promise to make users better.

It promises something more subtle and more valuable:

> **To warn users when their current trajectory is becoming structurally unreliable — early enough that they still have agency.**

That is the v1 intelligence contract.

---
