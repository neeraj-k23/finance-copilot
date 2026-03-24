from backend.services.analytics import get_overspending


def z_to_text(z):
    if z > 2:
        return "much higher than usual"
    elif z > 1:
        return "slightly higher than usual"
    elif z < -2:
        return "significantly lower than usual"
    elif z < -1:
        return "lower than usual"
    else:
        return "within your normal range"


def generate_insights():
    data = get_overspending()

    insights = []

    for item in data:
        category = item["category"]
        current = item["current_month"]
        mean = item["weighted_mean"]
        z = item["z_score"]
        status = item["status"]

        human_text = z_to_text(z)

        if status == "High Overspending":
            msg = (
                f"Your {category} spending is {human_text}. "
                f"You spent {current}, compared to your usual average of around {mean}. "
                f"This could indicate unusually high spending in this category."
            )

        elif status == "Above Normal":
            msg = (
                f"Your {category} spending is {human_text}. "
                f"Current spend is {current} vs your typical ~{mean}."
            )

        elif status == "Reduced Spending":
            msg = (
                f"Your {category} spending is {human_text}. "
                f"You spent {current}, which is below your usual level (~{mean})."
            )

        else:
            continue  # skip normal cases

        insights.append({
            "category": category,
            "message": msg,
            "status": status
        })

    return insights