"""
Responsibility:
Runs the weekly analytics and reporting pipeline.
"""

from pipelines.ingest import ingest_user
from pipelines.analyze import analyze_user
from pipelines.week_utils import split_into_weeks
from pipelines.generate_insights import generate_insights


def run_weekly_report(user_id: str) -> None:
    user = ingest_user(user_id)
    if not user:
        print(f"No data found for user '{user_id}'.")
        return

    analysis = analyze_user(user)

    daily_totals = analysis["daily_totals"]
    current_week, previous_week = split_into_weeks(daily_totals)

    current_week_total = sum(current_week.values())
    previous_week_total = (
        sum(previous_week.values()) if previous_week else None
    )

    insights = generate_insights(
        analysis,
        previous_week_total=previous_week_total,
    )

    print("\n📅 Weekly Report\n")
    print(f"Total active time this week: {current_week_total} minutes\n")

    if insights["weekly_summary"]:
        print("🧠 Weekly Insight:")
        print(insights["weekly_summary"], "\n")

    if insights["weekly_recommendations"]:
        print("💡 Recommendations:")
        for rec in insights["weekly_recommendations"]:
            print(f"- {rec}")


if __name__ == "__main__":
    run_weekly_report("synthetic_user")
