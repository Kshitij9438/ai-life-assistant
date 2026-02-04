from insights.warning_engine import evaluate_warning

def test_no_history_returns_none():
    result = evaluate_warning([], weeks_observed=0, confidence="moderate")
    assert result["warning_level"] == "none"
def test_single_r1_no_warning():
    result = evaluate_warning(["R1"], weeks_observed=1, confidence="moderate")
    assert result["warning_level"] == "none"
def test_recovery_resets_warning():
    result = evaluate_warning(["R0", "R1", "R0"], weeks_observed=3, confidence="moderate")
    assert result["warning_level"] == "none"
def test_first_persistence_watch():
    result = evaluate_warning(["R0", "R1", "R1"], weeks_observed=3, confidence="moderate")
    assert result["warning_level"] == "watch"
def test_escalation_triggers_caution():
    result = evaluate_warning(["R1", "R2"], weeks_observed=2, confidence="moderate")
    assert result["warning_level"] == "caution"
def test_persistent_high_risk_alert():
    result = evaluate_warning(["R1", "R2", "R2"], weeks_observed=3, confidence="high")
    assert result["warning_level"] == "alert"
def test_low_confidence_blocks_alert():
    result = evaluate_warning(["R1", "R2", "R2"], weeks_observed=3, confidence="low")
    assert result["warning_level"] != "alert"
def test_deescalation_after_recovery():
    result = evaluate_warning(["R2", "R2", "R0"], weeks_observed=3, confidence="high")
    assert result["warning_level"] == "none"
