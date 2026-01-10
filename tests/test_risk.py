from insights.risk import classify_weekly_risk
from insights.risk import detect_risk_transition

def test_classify_weekly_risk():
    # Test data for various risk levels
    test_cases = [
        # R0 - stable
        ({"dv": 0.1, "dr": 0.2, "cb": 0.5}, "R0"),
        # R1 - load concentration risk
        ({"dv": 0.1, "dr": 0.8, "cb": 0.5}, "R1"),
        ({"dv": 0.1, "dr": 0.2, "cb": 0.2}, "R1"),
        # R2 - volatility risk
        ({"dv": 0.8, "dr": 0.2, "cb": 0.5}, "R2"),
        # R3 - fragile trajectory
        ({"dv": 0.8, "dr": 0.8, "cb": 0.5}, "R3"),
        # R4 - insufficient signal
        ({}, "R4"),
    ]

    for features, expected_risk_level in test_cases:
        result = classify_weekly_risk(features)
        assert result["risk_level"] == expected_risk_level, f"Failed for features: {features}"
def test_detect_risk_transition():
    test_cases = [
        ({"risk_level": "R0"}, {"risk_level": "R1"}, "increasing_risk"),
        ({"risk_level": "R2"}, {"risk_level": "R1"}, "decreasing_risk"),
        ({"risk_level": "R1"}, {"risk_level": "R1"}, "stable"),
        (None, {"risk_level": "R1"}, "unknown"),
        ({"risk_level": "R1"}, None, "unknown"),
    ]

    for prev, curr, expected_transition in test_cases:
        result = detect_risk_transition(prev, curr)
        assert result == expected_transition, f"Failed for prev: {prev}, curr: {curr}"