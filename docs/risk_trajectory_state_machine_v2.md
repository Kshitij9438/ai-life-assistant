# AI Life Assistant — Risk Trajectory State Machine (v2)

## Status

* Version: v2
* Scope: Weekly risk trajectory evaluation
* Depends on: `risk_taxonomy_v1.1`
* Governs: Warning emission logic
* Backward compatibility: Fully compatible with v1

---

## Purpose

This document defines the **deterministic state machine** used to
translate weekly risk classifications into **early warning signals**.

It governs **when the system is allowed to warn**, and more importantly,
**when it must remain silent**.

---

## Scope

This state machine operates **only at weekly resolution** and consumes:

* **Risk states** from v1: `{R0, R1, R2, R3, R4}`
* **Ordered history** of recent weeks (most recent last)

It outputs **one of four warning states**:

```
none | early_warning | elevated_warning | critical_warning
```

---

## 1️⃣ Inputs

### Required Inputs

* `risk_history`: ordered list of weekly risk levels
  Example:

```python
["R0", "R1", "R1"]
```

### Minimum History Requirement

* **At least 3 consecutive weeks**
* If fewer than 3 weeks exist → **return `none`**

This enforces the **anti-reactivity principle**.

---

## 2️⃣ Normalization Rules

Before evaluation:

### Rule N1 — R4 Uncertainty Barrier

* `R4` represents *insufficient signal*
* **If any `R4` exists in the last 3 weeks → return `none`**

> **Clarification**
> R4 is treated as a **hard uncertainty barrier**.
> Warnings must not cross weeks with insufficient signal, even if adjacent weeks are risky.

### Rule N2 — Short Memory Window

* Only the **last N = 3 weeks** are considered
* v2 intentionally uses a short memory to keep warnings reversible

---

## 3️⃣ Pattern Matching Semantics (Important)

Let:

```
W-2, W-1, W0
```

be the **three most recent risk states**, where `W0` is the current week.

> **Clarification**
> Trajectory patterns are matched against the **most recent contiguous suffix**
> of the last three weeks.
>
> Example:
>
> ```
> [R0, R2, R2] → matches [R2, R2]
> ```

This avoids ambiguity and ensures deterministic evaluation.

---

## 4️⃣ Warning Resolution Order (Strict)

Warnings are resolved in **strict priority order**:

```
critical_warning
→ elevated_warning
→ early_warning
→ none
```

The **first matching rule wins**.
No lower-priority rule may override a higher one.

---

## 5️⃣ Critical Warning Rules 🔴

### Rule C1 — Sustained Fragility

```
[R3, R3]
```

or

```
[R2, R3, R3]
```

**Meaning**

> Fragility is not transient; structural failure is likely.

**Output**

```json
{
  "level": "critical",
  "reason": "Sustained fragile trajectory across multiple weeks"
}
```

---

### Rule C2 — Escalating Collapse

```
[R1, R2, R3]
```

**Meaning**

> Rapid deterioration across consecutive weeks.

**Output**

```json
{
  "level": "critical",
  "reason": "Rapid escalation from moderate risk to fragility"
}
```

---

## 6️⃣ Elevated Warning Rules 🟠

### Rule E1 — Persistent Volatility

```
[R2, R2]
```

or

```
[R1, R2, R2]
```

**Meaning**

> Instability is failing to self-correct.

**Output**

```json
{
  "level": "elevated",
  "reason": "Volatility persists without recovery"
}
```

---

### Rule E2 — Transition Into Fragility

```
[R2, R3]
```

**Meaning**

> System crossed into fragile territory.

**Note**

If this transition is part of a longer escalation (e.g. `R1 → R2 → R3`),
**Rule C2 takes precedence**.

**Output**

```json
{
  "level": "elevated",
  "reason": "Transition from volatility to fragile trajectory"
}
```

---

## 7️⃣ Early Warning Rules 🟡

### Rule W1 — Risk Emergence

```
[R0, R1, R1]
```

**Meaning**

> Early concentration or imbalance forming.

**Output**

```json
{
  "level": "early",
  "reason": "Risk emerging across consecutive weeks"
}
```

---

### Rule W2 — Upward Drift

```
[R1, R2]
```

**Meaning**

> Drift from concentration into instability.

**Output**

```json
{
  "level": "early",
  "reason": "Upward drift toward volatility"
}
```

---

### Rule W3 — Sustained Moderate Risk

```
[R2, R2]
```

*(only if not caught by elevated rules)*

**Meaning**

> Risk present but not escalating.

---

## 8️⃣ Explicit Silence Rules ⚪

### Rule S1 — Improvement

Any sequence where:

```
W0 < W-1
```

Examples:

```
[R2 → R1]
[R3 → R2]
```

→ **return `none`**

---

### Rule S2 — Oscillation Without Trend

Examples:

```
[R1, R0, R1]
[R2, R1, R2]
```

→ **return `none`**

---

### Rule S3 — Stable or Low Risk

Any sequence where:

```
max(risk_history) ≤ R1
```

→ **return `none`**

---

## 9️⃣ Output Schema (Formal)

The state machine must return:

```json
{
  "warning_level": "none" | "early" | "elevated" | "critical",
  "reason": string | null,
  "trajectory": ["R1", "R2", "R2"],
  "weeks_observed": 3
}
```

If `warning_level == "none"`:

* `reason = null`

---

## 10️⃣ Invariants (Must Always Hold)

1. **No warning on single-week spikes**
2. **No warning with insufficient data**
3. **Warnings are reversible**
4. **Removing the oldest week can remove a warning**
5. **State machine is deterministic**
6. **Uncertainty blocks escalation**

---

## 11️⃣ Why This Design Fits This System

This state machine:

* aligns exactly with the **risk taxonomy**
* preserves **epistemic humility**
* avoids emotional escalation
* allows silence to dominate
* scales cleanly to monthly horizons later

Most importantly:

> **It treats warnings as *rare events*, not features.**

---

