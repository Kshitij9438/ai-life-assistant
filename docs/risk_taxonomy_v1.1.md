# AI Life Assistant — Formal Risk Taxonomy (v1.1)

## Purpose

This taxonomy defines **structural risk states** inferred from observed behavior patterns.

It does **not** infer:

* mental state
* motivation
* intent
* health
* productivity quality

It classifies **trajectory risk**, not outcomes.

All thresholds assume raw (non-normalized) feature values as produced by the analytics pipeline.
---

## Core Principle

> **Risk is defined as the likelihood that current behavior cannot be sustained without involuntary change.**

“Involuntary change” includes:

* collapse
* abrupt reduction
* forced rebalancing
* unplanned disengagement

---

## Risk Axes (Foundational)

All risk states are derived from **three orthogonal axes**:

### 1️⃣ Variability Axis — *Stability of execution*

Measured by:

* `daily_variability`

Represents:

* predictability
* rhythm consistency
* load volatility

---

### 2️⃣ Dominance Axis — *Concentration of load*

Measured by:

* `dominance_ratio`
* `category_dominance_ratio`

Represents:

* single-point dependency
* over-reliance on one activity or category

---

### 3️⃣ Balance Axis — *Distribution of effort*

Measured by:

* `category_balance`

Represents:

* diversification
* resilience to disruption

---

## Canonical Risk States (v1.1)

The system may classify **exactly one primary risk state per week**.

---

## 🟢 R0 — Stable Trajectory

### Definition

A pattern that is **structurally sustainable** under small perturbations.

### Signal Profile

* Low variability
* Low dominance
* Moderate to high balance

### Formal Conditions (example)

```text
daily_variability < V₁
AND dominance_ratio < D₁
```

### Interpretation

> “This trajectory is internally consistent and resilient.”

### System Behavior

* Normal prediction
* High trust in explanation
* No warning signals

---

## 🟡 R1 — Load Concentration Risk

### Definition

A pattern where **too much load depends on too few sources**, even if total volume is stable.

### Signal Profile

* Moderate variability
* High dominance
* Low category balance

### Formal Conditions

```text
dominance_ratio ≥ D₂
AND daily_variability < V₂
```

### Interpretation

> “This trajectory works, but has a single point of failure.”

### Typical Cause

* One activity dominating time
* One category absorbing most effort

### System Behavior

* Prediction allowed
* Confidence marked as *fragile*
* Explanation emphasizes dominance drivers

---

## 🟠 R2 — Volatility Risk

### Definition

A pattern with **unstable execution**, regardless of total volume.

### Signal Profile

* High variability
* Moderate or low dominance

### Formal Conditions

```text
daily_variability ≥ V₃
AND dominance_ratio < D₂
```

### Interpretation

> “This trajectory lacks rhythm; persistence is unreliable.”

### Typical Cause

* Irregular schedules
* Bursty engagement
* Overcompensation cycles

### System Behavior

* Prediction allowed with caution
* Explanation emphasizes variability drivers
* Lower confidence in week-to-week continuity

---

## 🔴 R3 — Fragile Trajectory

### Definition

A pattern that is **both concentrated and volatile**.

### Signal Profile

* High variability
* High dominance
* Low balance

### Formal Conditions

```text
daily_variability ≥ V₃
AND dominance_ratio ≥ D₂
```

### Interpretation

> “This trajectory is structurally unstable and likely to break.”

### Typical Cause

* Overload in a single domain
* Unsustainable pacing
* Short-term surges

### System Behavior

* Prediction still computed
* Confidence explicitly marked *fragile*
* System highlights risk prominently
* No prescriptive advice given

---

## ⚫ R4 — Insufficient Signal (Refusal State)

### Definition

The system cannot reliably assess trajectory risk.

### Causes

* < 2 weeks of data
* Near-zero activity
* Highly sparse logs

### Interpretation

> “No valid inference can be made.”

### System Behavior

* No prediction
* No explanation
* Explicit refusal

---

## Risk vs Confidence Mapping

| Risk State | confidence_hint |
| ---------- | --------------- |
| R0         | stable          |
| R1         | moderate        |
| R2         | moderate        |
| R3         | fragile         |
| R4         | —               |

Confidence reflects **trajectory reliability**, not correctness.

---

## Guarantees

* Risk states are:

  * deterministic
  * testable
  * explainable
* No state implies moral judgment
* No state implies recommendation

---

## Explicit Non-Claims

This taxonomy does **not** claim to detect:

* burnout
* motivation loss
* stress
* success probability
* well-being

Those may be *downstream interpretations*, not v1 outputs.

---

## Why This Taxonomy Works

1. **Maps directly to your existing features**
2. **Explains *why* a trajectory is risky**
3. **Supports early warning without prediction inflation**
4. **Allows silence as intelligence**
5. **Scales cleanly to monthly horizons later**

---

## v1.1 Completion Criteria

The taxonomy is considered implemented when:

* Each weekly report includes:

  * a primary risk state
  * supporting signals
* Risk state is derived mechanically
* Risk is explained, not predicted

---

## Final Note (Important)

This taxonomy is not a diagnosis system.

It is a **structural warning system**.

> *It does not tell users what they are doing wrong —
> it tells them when their current pattern is becoming unreliable.*

That distinction is why this system has integrity.

---
