# AI Life Assistant  
### Behavioral Risk Intelligence System

This repository implements a **personal behavioral intelligence system** that models **risk as a trajectory over time**, detects **behavioral drift**, and issues **early warnings** using primarily **passive signals**.

This project is **not** a productivity tool, habit tracker, chatbot, or motivational system.  
It is a **longitudinal risk modeling engine** designed to reason cautiously about how human behavior evolves — and when that evolution becomes fragile.

---

## The problem this system models

Most personal systems ask:

> “What should the user do?”

This system asks a different, more fundamental question:

> **“Given observed behavior over time, what does the system believe about the stability of the current trajectory — and how is that belief changing?”**

The focus is **not outcomes, intent, or psychology**, but **structural sustainability of behavior**.

---

## Core idea

Human behavior is treated as a **dynamic system under uncertainty**.

Rather than reacting to individual events, the system:

1. **Observes behavioral signals over time**
2. **Infers latent stability states**
3. **Tracks risk as a trajectory, not a score**
4. **Estimates short-horizon drift**
5. **Emits early warnings only when confidence is sufficient**

Silence and refusal are considered **correct outputs** when evidence is weak.

---

## Key abstractions

### Signals

Signals are any observable behavioral evidence emitted over time, including:

- activity regularity  
- load concentration  
- volatility  
- gaps, delays, and structural imbalance  

Signals are **passive-first** and do not rely on constant user input.

---

### State

A state represents the system’s **current belief** about behavioral stability.

States are:

- inferred (never self-reported)  
- time-dependent  
- deterministic given sufficient signal  
- explicitly bounded by refusal conditions  

---

### Risk trajectory

Risk is **not a snapshot** and **not a score**.

It is a **trajectory**:

- direction matters  
- acceleration matters  
- volatility matters  

The system cares more about **where risk is heading** than where it currently is.

---

### Warning semantics

Warnings are emitted only when:

- trajectories cross structural thresholds  
- drift is consistent across signals  
- early correction is still possible  

The system prefers **early, low-cost warnings** over late or intrusive intervention.

---

## What this system explicitly does *not* do

This project does **not**:

- optimize productivity  
- prescribe actions or schedules  
- motivate users  
- infer intent, discipline, or effort  
- predict success, burnout, or well-being  
- produce long-horizon forecasts  
- speak when signal quality is insufficient  

These are **intentional design constraints**, not missing features.

---

## System behavior (current scope)

### Weekly behavioral intelligence

- Aggregates daily behavior into weekly signals  
- Produces **short-horizon (next-week) projections only**  
- Treats baselines as first-class references  
- Suppresses ML output when it adds no structural value  

---

### Baseline-first reasoning

- Baseline error is always computed  
- Model error is always compared against baseline  
- ML is treated as **non-authoritative**  
- If ML does not outperform baseline, it is demoted  

---

### Explainability

All projections include:

- numeric feature contributions  
- deltas vs baseline and prior period  
- structurally grounded confidence hints  

No black-box explanations.  
No behavioral judgments.

---

### Risk state classification

Behavioral trajectories are classified into deterministic states:

- **R0** — Stable trajectory  
- **R1** — Load concentration risk  
- **R2** — Volatility risk  
- **R3** — Fragile trajectory  
- **R4** — Insufficient signal (explicit refusal)  

Risk reflects **structural sustainability**, not outcomes or psychology.

---

### Refusal semantics

When signal quality is insufficient, the system returns:

```json
{
  "state": "insufficient_data"
}
````

No prediction.
No explanation.

This is **correct behavior**.

---

## Architecture (high-level)

```
Behavioral signals
        ↓
Aggregation & structure analysis
        ↓
Baseline evaluation
        ↓
Optional interpretable ML
        ↓
Trajectory estimation
        ↓
Risk state classification
        ↓
Warning / refusal
```

Daily processing is **descriptive only** and intentionally non-predictive.

---

## Machine learning philosophy

* **Model**: Interpretable linear models
* **Role**: Assist reasoning, never dominate it
* **Authority**: Baselines first, ML second
* **Failure mode**: Safe refusal

ML is a **component**, not the identity of the system.

---

## Project structure

```
ai-life-assistant/
├── core/            # Domain entities
├── analytics/       # Aggregation & structural signals
├── insights/        # State, trajectory, warnings
├── ml/              # Interpretable models & evaluation
├── pipelines/       # Longitudinal orchestration
├── scripts/         # Entry points
├── docs/            # Intelligence contracts & taxonomies
├── tests/           # Behavioral & invariant tests
```

Minimal or empty modules represent **stable conceptual boundaries**, not incomplete work.

---

## Intelligence contract

System behavior is governed by explicit contracts:

* `docs/intelligence_contract_v*.md`
* `docs/risk_trajectory_state_machine_v*.md`

Code is considered correct **only if it conforms to these contracts**.

---

## Status

**Canonical branch: `main`**

The system is considered valid when:

* trajectories are time-consistent
* baselines are enforced
* risk states are deterministic
* refusal semantics are honored

Future versions may expand signal sources, but **the modeling philosophy is stable**.

---

## Author

**Kshitij**

Built as a serious exploration of:

* behavioral risk modeling
* longitudinal intelligence systems
* epistemic humility in ML

---

## License

MIT

