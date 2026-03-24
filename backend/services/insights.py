from backend.services.analytics import get_overspending


def generate_insights():
    data = get_overspending()

    insights = []

    for item in data:
        category = item["category"]
        avg_change = item["avg_change_percent"]
        prev_change = item["prev_change_percent"]
        status = item["status"]

        if status == "High Overspending":
            msg = (
                f"Your {category} spending is significantly higher than usual "
                f"({round(avg_change, 1)}% above average). Consider reviewing your expenses."
            )

        elif status == "Recent Spike":
            msg = (
                f"There is a recent spike in your {category} spending "
                f"({round(prev_change, 1)}% increase from last month)."
            )

        elif status == "Above Average":
            msg = (
                f"Your {category} spending is higher than your usual pattern "
                f"({round(avg_change, 1)}% above average)."
            )

        elif status == "Reduced Spending":
            msg = (
                f"Good job! Your {category} spending has decreased significantly."
            )

        else:
            continue

        insights.append({
            "category": category,
            "message": msg,
            "status": status
        })

    return insights