# scripts/run_weekly_intelligence.py
from pipelines.run_weekly_intelligence import run_weekly_intelligence
from pprint import pprint

if __name__ == "__main__":
    report = run_weekly_intelligence("synthetic_user")
    pprint(report)
