# AI Life Assistant

An end-to-end, modular AI system for analyzing daily activities, generating insights and recommendations, and predicting future behavior using interpretable machine learning.

This project is designed as a **production-style analytics + ML pipeline**, not a notebook experiment.

---

## 🚀 What This Project Does

The AI Life Assistant:

- Logs and aggregates daily activity data
- Generates human-readable **insights** and **recommendations**
- Learns behavioral patterns using **interpretable linear regression**
- Predicts **tomorrow’s total activity time**
- Runs entirely via a **clean CLI pipeline**

---

## 🧠 System Overview

```

Data → Analytics → Insights → Recommendations → ML Prediction

```

### Core capabilities:
- **Analytics**: daily & weekly aggregations, trends
- **Insights**: natural-language summaries of behavior
- **Recommendations**: rule-based behavioral suggestions
- **ML**: causal, time-aware regression with lag features
- **CLI**: daily and weekly reports

---

## 📁 Project Structure

```

ai-life-assistant/
├── core/           # Domain models (Activity, DayLog, User)
├── analytics/      # Aggregations, trends, statistics
├── insights/       # Summaries & recommendations
├── ml/             # Features, datasets, models, evaluation
├── pipelines/      # Orchestration logic
├── scripts/        # CLI entry points
├── tests/          # Unit tests
├── data/            # (ignored) generated data
├── reports/         # (ignored) generated outputs

```

Empty modules are **intentional** and represent planned system boundaries.

---

## 🔮 Machine Learning Approach

- **Model**: Linear Regression (Ordinary Least Squares)
- **Why**: Interpretability > complexity
- **Features**:
  - Daily activity totals
  - Category-level minutes
  - Lag features (previous day, rolling averages)
- **Target**:
  - Next day’s total activity time

The model is evaluated using **MAE** and **RMSE**, and predictions are integrated directly into the daily report.

---

## 🖥️ Example Output

```

📅 Daily Report — 2026-01-06

Total active time: 3h 15m

By category:

* Leisure: 2h 15m
* Work: 1h 0m

🧠 Insight:
Leisure dominated your day, accounting for most of your active time.

💡 Recommendations:

* Consider balancing leisure with lighter productive activities.

🔮 Prediction:
Estimated total activity for tomorrow: 8.3 hours

````

---

## ▶️ How to Run

### 1. Set up environment
```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
````

### 2. Generate synthetic data

```bash
python -m scripts.generate_data
```

### 3. Run daily report

```bash
python -m scripts.run_daily
```

---

## 🧪 Tests

```bash
pytest
```

---

## 🎯 Design Philosophy

* **Architecture first** (clear module boundaries)
* **Data realism over model complexity**
* **Causal, time-aware ML**
* **No black boxes**
* **Production-style project layout**

---

## 📌 Status

This project is intentionally extensible.
Planned areas include:

* Correlation analysis
* Advanced statistics
* Model regularization
* Weekly ML predictions
* API interface

---

## 👤 Author

**Kshitij**
Built as a hands-on exploration of real-world AI system design.

---

## 📜 License

MIT
```
