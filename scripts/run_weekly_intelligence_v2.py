# scripts/run_weekly_intelligence_v2.py

from pipelines.run_weekly_intelligence_v2 import run_weekly_intelligence_v2
from pprint import pprint

if __name__ == "__main__":
    report = run_weekly_intelligence_v2(
        "synthetic_user",
        risk_history=["R0", "R1"]  # example history
    )
    pprint(report)
