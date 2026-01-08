from insights.explainations import explain_weekly_prediction

def test_deltas_are_correct():
    expl = explain_weekly_prediction(
        features={"daily_variability": 25.0, "dominance_ratio": 0.4},
        coefficients={"daily_variability": 1.0, "dominance_ratio": 2.0},
        baseline_value=100.0,
        previous_week_value=95.0,
        prediction=110.0
    )
    assert expl["prediction"] - expl["baseline"] == expl["delta_vs_baseline"]

def test_top_driver_is_max_contribution():
    expl = explain_weekly_prediction(
        features={"daily_variability": 25.0, "dominance_ratio": 0.4},
        coefficients={"daily_variability": 1.0, "dominance_ratio": 2.0},
        baseline_value=100.0,
        previous_week_value=95.0,
        prediction=110.0
    )
    contribs = expl["feature_contributions"]
    top = expl["top_positive_drivers"][0][0]
    assert abs(contribs[top]) == max(abs(v) for v in contribs.values())

def test_confidence_fragile_when_dominance_high():
    expl = explain_weekly_prediction(
        features={"daily_variability": 25.0, "dominance_ratio": 0.9},
        coefficients={"daily_variability": 1.0, "dominance_ratio": 2.0},
        baseline_value=100.0,
        previous_week_value=95.0,
        prediction=110.0
    )
    assert expl["confidence_hint"] == "fragile"
