# AI Life Assistant
“v2-risk-trajectory is an experimental branch exploring early warning semantics. Not intended for merge into main yet."

A **baseline-aware, explainable behavioral intelligence system** for detecting and forecasting the *structural sustainability* of human activity patterns.

This project is **not** a productivity tool, habit tracker, or motivational system.
It is a **decision-support intelligence engine** designed to reason cautiously about behavior over time.

---

## What This System Does (Precisely)

At its core, the AI Life Assistant answers one question:

> **“Given recent behavior, is the current activity trajectory stable, fragile, or at risk — and why?”**

To do this, the system:

* Aggregates daily activity logs into structured weekly signals
* Evaluates behavior **relative to explicit baselines**
* Produces **short-horizon forecasts only** (weekly)
* Explains predictions using **fully numeric, additive explanations**
* Classifies **structural risk states** deterministically
* Explicitly **refuses to speak** when signal quality is insufficient

Silence is considered a **correct and intentional output**.

---

## What This System Explicitly Does *Not* Do

This project does **not**:

* optimize productivity
* prescribe schedules or actions
* motivate users
* infer intent, discipline, or effort
* predict burnout, success, or well-being
* produce long-horizon forecasts
* perform daily-level prediction

These exclusions are **deliberate design choices**, not missing features.

---

## Core Capabilities (v1)

### 🧠 Weekly Behavioral Intelligence

* Computes weekly activity totals and structure
* Forecasts **next week only**
* Always compares predictions against a naive baseline
* Downgrades or suppresses ML output when it adds no value

### 📉 Baseline-Aware Evaluation

* Baseline MAE is always computed
* Model MAE is always computed (when ML is used)
* The system explicitly reports whether ML beats the baseline
* If it does not, ML is treated as **non-authoritative**

### 🧩 Explainable Predictions

Every prediction includes:

* numeric feature contributions
* top positive and negative drivers
* explicit deltas vs baseline and previous week
* confidence hints tied to structural reliability

No black-box explanations.
No behavioral judgments.

### ⚠️ Structural Risk Classification

Weekly behavior is classified into deterministic risk states:

* **R0** — Stable trajectory
* **R1** — Load concentration risk
* **R2** — Volatility risk
* **R3** — Fragile trajectory
* **R4** — Insufficient signal (refusal)

Risk reflects **trajectory sustainability**, not outcomes or psychology.

### 🛑 Refusal Semantics

If fewer than two full weeks of data exist — or signal quality is poor — the system returns:

```json
{
  "state": "insufficient_data"
}
```

No prediction.
No explanation.

This is correct behavior.

---

## System Architecture (High-Level)

```
Ingestion
   ↓
Analytics (aggregation, variability, balance)
   ↓
Baseline evaluation
   ↓
Optional ML (interpretable, non-authoritative)
   ↓
Numeric explanation
   ↓
Risk classification
   ↓
Weekly intelligence report
```

Daily processing is **descriptive only** and intentionally non-predictive.

---

## Machine Learning Philosophy

* **Model**: Linear Regression (OLS)
* **Reason**: Interpretability > complexity
* **Role of ML**: Assist explanations, never dominate decisions
* **Authority**: Baselines first, ML second
* **Failure Mode**: Safe refusal

ML is treated as a **component**, not the identity of the system.

---

## Project Structure

```
ai-life-assistant/
├── core/            # Domain entities (Activity, DayLog, User)
├── analytics/       # Aggregations, statistics, trends
├── insights/        # Explanations, risk, summaries
├── ml/              # Interpretable models & evaluation
├── pipelines/       # End-to-end orchestration
├── scripts/         # CLI entry points
├── docs/            # Intelligence contract & risk taxonomy
├── tests/           # Unit + behavioral tests
```

Empty or minimal modules are **intentional** and represent stable system boundaries.

---

## Intelligence Contract

The system is governed by an explicit contract:

* [`docs/intelligence_contract_v1.md`](docs/intelligence_contract_v1.md)
* [`docs/risk_taxonomy_v1.1.md`](docs/risk_taxonomy_v1.1.md)

These documents define:

* scope
* guarantees
* refusal conditions
* non-goals

Code is considered correct **only if it conforms to the contract**.

---

## Running the System

### 1. Environment setup

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Generate synthetic data

```bash
python -m scripts.generate_data
```

### 3. Run weekly intelligence

```bash
python -m scripts.run_weekly_intelligence
```

Daily reports are available but **do not perform prediction** by design.

---

## Testing Philosophy

Tests verify:

* numerical correctness
* invariants and refusal conditions
* deterministic risk classification
* baseline vs model behavior
* explanation consistency

This is not just unit testing — it is **behavioral testing**.

---

## Status

**v1.0 — Frozen Intelligence Contract**

The system is considered complete when:

* weekly pipeline runs end-to-end
* baseline awareness is enforced
* explanations are additive and testable
* risk classification is deterministic
* refusal semantics are honored

Future versions may extend scope, but **v1 behavior is frozen**.

---

## Author

**Kshitij**

Built as a serious exploration of:

* explainable AI
* epistemic humility in ML
* behavioral intelligence system design

---

## License

MIT

---



