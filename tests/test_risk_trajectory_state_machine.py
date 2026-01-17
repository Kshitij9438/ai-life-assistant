from insights.risk_trajectory import evaluate_risk_trajectory


def test_no_warning_with_insufficient_history():
    assert evaluate_risk_trajectory(["R1", "R2"])["warning_level"] == "none"


def test_no_warning_with_r4_present():
    assert evaluate_risk_trajectory(["R2", "R4", "R2"])["warning_level"] == "none"


def test_early_warning_emergence():
    result = evaluate_risk_trajectory(["R0", "R1", "R1"])
    assert result["warning_level"] == "early"


def test_elevated_persistent_volatility():
    result = evaluate_risk_trajectory(["R1", "R2", "R2"])
    assert result["warning_level"] == "elevated"


def test_critical_escalation():
    result = evaluate_risk_trajectory(["R1", "R2", "R3"])
    assert result["warning_level"] == "critical"


def test_silence_on_improvement():
    result = evaluate_risk_trajectory(["R3", "R2", "R1"])
    assert result["warning_level"] == "none"


def test_silence_on_oscillation():
    result = evaluate_risk_trajectory(["R1", "R0", "R1"])
    assert result["warning_level"] == "none"
