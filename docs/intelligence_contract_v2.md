# AI Life Assistant — Intelligence Contract (v2: Early Warning)

## Status

**Version:** v2 (extends v1.0)
**Branch:** `v2-risk-trajectory`
**Compatibility:** Fully backward-compatible with v1
**Scope:** Weekly intelligence + early warning semantics

---

## Purpose (v2 Refinement)

Version 2 extends the v1 intelligence contract with **early warning capability**.

The purpose of v2 is:

> **To detect *emerging instability* in a user’s behavioral trajectory early enough that corrective action is still optional, not forced.**

This system remains a **decision-support intelligence**, not a recommendation engine, therapist, or productivity tool.

---

## Continuity with v1 (Non-Negotiable)

All v1 guarantees **remain in force**, including:

* baseline humility
* refusal semantics
* explainability-first design
* short-horizon reasoning
* weekly resolution

**If v2 behavior conflicts with v1, v1 wins.**

---

## New Intelligence Question (v2)

v2 introduces exactly one new class of question:

> **“Is the user’s risk profile *changing in a way that warrants attention* — and if so, how urgently?”**

This is **trajectory intelligence**, not state classification.

---

## Definitions

### Risk State (from v1)

A weekly classification in `{R0, R1, R2, R3, R4}` describing **structural sustainability**.

### Risk Trajectory (v2)

An ordered sequence of recent weekly risk states, e.g.:

```
[R0 → R1 → R1]
[R1 → R2]
[R2 → R3]
```

Risk trajectory is the **primary input** to warnings.

---

## Warning Philosophy (Core Principle)

> **Warnings are issued based on *patterns*, not single observations.**

A single risky week is **not sufficient** to warn.

Warnings are:

* conservative
* explainable
* reversible
* rare by design

Silence remains a valid and preferred outcome.

---

## Warning States (v2)

The system may emit **at most one warning per week**, chosen from:

### ⚪ `none` — No Warning (Default)

**Definition**

* Risk is stable or improving
* Or signal strength is insufficient
* Or risk is transient

**Guarantee**

* Most weeks produce no warning

---

### 🟡 `early_warning`

**Definition**

* Risk has increased *or persisted* across multiple weeks
* But trajectory is not yet fragile

**Typical Patterns**

* `R0 → R1 → R1`
* `R1 → R2`
* `R2` sustained for ≥ 2 weeks

**Interpretation**

> “This trajectory is drifting toward instability, but remains recoverable.”

**System Behavior**

* Prediction allowed
* Explanation required
* No urgency language

---

### 🟠 `elevated_warning`

**Definition**

* Risk is clearly worsening or failing to resolve

**Typical Patterns**

* `R1 → R2 → R2`
* `R2 → R3`
* `R3` sustained for ≥ 2 weeks

**Interpretation**

> “This trajectory shows structural instability that may soon force change.”

**System Behavior**

* Prediction allowed
* Confidence marked *fragile*
* Warning highlighted but non-prescriptive

---

### 🔴 `critical_warning`

**Definition**

* Sustained fragile trajectory

**Typical Patterns**

* `R3 → R3`
* `R2 → R3 → R3`

**Interpretation**

> “This trajectory is unlikely to sustain without involuntary change.”

**System Behavior**

* Prediction allowed
* Warning emphasized
* System still does **not** prescribe actions

---

## Warning Output Contract

When a warning is emitted, the weekly report includes:

```json
"warning": {
  "level": "early" | "elevated" | "critical",
  "reason": string,
  "trajectory": ["R1", "R2", "R2"],
  "weeks_observed": int
}
```

### Guarantees

* Warning reason must reference **risk trajectory**, not user intent
* Warning must be explainable from prior outputs
* No warnings are emitted for `R4`

---

## Silence & Refusal (Extended)

v2 **must not** warn when:

* fewer than 3 weeks of data exist
* risk state is improving
* risk oscillates without trend
* signal quality is low

Silence is **preferred over premature warning**.

---

## Non-Goals (v2 Explicit)

Version 2 does **not**:

* predict burnout
* assess mental health
* assign blame or causality
* recommend behavioral changes
* escalate emotionally
* operate below weekly resolution

Warnings are **informational**, not motivational.

---

## Evaluation Criteria (v2)

v2 is considered correct if:

* warnings are rare
* false positives are minimized
* warnings are consistent across re-runs
* removing 1 week of data can *remove* a warning
* explanations remain numeric and structural

---

## Relationship to Future Versions

This contract **intentionally enables**:

* v3: adaptive thresholds
* v4: user-calibrated sensitivity
* v5: multi-timescale risk fusion

But v2 itself remains **conservative and minimal**.

---

## Final Principle (v2)

> **A late warning is acceptable.
> A false warning is not.**

This principle overrides all optimization goals.

---

## Version Status

* **v1**: Frozen
* **v2**: Active development
* **Scope**: Early warning only

