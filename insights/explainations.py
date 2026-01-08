def explain_weekly_prediction(
    features: dict[str, float],
    coefficients: dict[str, float],
    baseline_value: float,
    previous_week_value: float,
    prediction: float,
    *,
    enforce_conservation: bool = False,
) -> dict:
    """
    Produce a structured explanation of a weekly prediction.

    Returns a fully numeric, testable explanation object.
    """
    delta_vs_baseline = prediction - baseline_value
    delta_vs_previous = prediction - previous_week_value
    contributions = {
    name: features[name] * coefficients.get(name, 0.0)
    for name in features}
    top_positive = sorted(
    [(k, v) for k, v in contributions.items() if v > 0],
    key=lambda x: abs(x[1]),
    reverse=True,)[:2]
    top_negative = sorted(
    [(k, v) for k, v in contributions.items() if v < 0],
    key=lambda x: abs(x[1]),
    reverse=True,)[:2]
    daily_var = features.get("daily_variability", 0.0)
    dom_ratio = features.get("dominance_ratio", 0.0)
    if daily_var < 30 and dom_ratio < 0.5:
        confidence = "stable"
    elif dom_ratio > 0.7:
        confidence = "fragile"
    else:
        confidence = "moderate"
    # Only enforce conservation when explanation is model-faithful
    if enforce_conservation:
        explained_delta = sum(contributions.values())
        model_delta = prediction - baseline_value
        if abs(explained_delta) > 0:
            ratio = model_delta / explained_delta
            assert 0.9 <= ratio <= 1.1


    return {
    "prediction": prediction,
    "baseline": baseline_value,
    "previous_week": previous_week_value,

    "delta_vs_baseline": delta_vs_baseline,
    "delta_vs_previous": delta_vs_previous,

    "feature_contributions": contributions,
    "top_positive_drivers": top_positive,
    "top_negative_drivers": top_negative,

    "confidence_hint": confidence,
    "total_contribution": sum(contributions.values()),

}


