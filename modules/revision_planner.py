from collections import defaultdict


# =========================================================
# 11. PERSONALIZED REVISION PLAN
# =========================================================

def generate_revision_plan(report, days, hours_per_day):

    total_hours = days * hours_per_day

    ranked_topics = sorted(
        report.items(),
        key=lambda item: item[1]["priority"],
        reverse=True
    )

    # Allocate time proportionally to priority.
    weights = [
        max(data["priority"], 1)
        for _, data in ranked_topics
    ]

    total_weight = sum(weights)

    allocations = [
        total_hours * weight / total_weight
        for weight in weights
    ]

    print("\n========== PERSONALIZED REVISION PLAN ==========")

    print(f"Available days: {days}")
    print(f"Hours per day: {hours_per_day}")
    print(f"Total study hours: {total_hours}")

    daily_plan = defaultdict(list)

    for (topic, data), allocated_hours in zip(
        ranked_topics, allocations
    ):

        remaining = allocated_hours

        for day in range(1, days + 1):

            if remaining <= 0:
                break

            already_used = sum(
                item["hours"]
                for item in daily_plan[day]
            )

            available = max(
                0,
                hours_per_day - already_used
            )

            if available <= 0:
                continue

            assigned = min(
                remaining,
                available
            )

            daily_plan[day].append({
                "topic": topic,
                "hours": assigned,
                "status": data["status"]
            })

            remaining -= assigned

    for day in range(1, days + 1):

        print(f"\nDAY {day}")

        if not daily_plan[day]:
            print("Revision and practice buffer")
            continue

        for item in daily_plan[day]:

            print(
                f"- {item['topic']}: "
                f"{item['hours']:.2f} hours "
                f"({item['status']})"
            )

    return daily_plan
