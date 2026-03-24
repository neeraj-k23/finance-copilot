import math
from backend.models.db import get_connection


def get_monthly_spend():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            DATE_FORMAT(date, '%Y-%m') as month,
            SUM(CASE WHEN type = 'debit' THEN amount ELSE 0 END) as total_spend
        FROM transactions
        GROUP BY month
        ORDER BY month;
    """)

    results = cursor.fetchall()
    conn.close()

    return [
        {"month": row[0], "total_spend": float(row[1] or 0)}
        for row in results
    ]


def get_category_breakdown():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            category,
            SUM(CASE WHEN type = 'debit' THEN amount ELSE 0 END) as total
        FROM transactions
        GROUP BY category
        ORDER BY total DESC;
    """)

    results = cursor.fetchall()
    conn.close()

    return [
        {"category": row[0], "amount": float(row[1] or 0)}
        for row in results
    ]





def get_overspending():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            category,
            DATE_FORMAT(date, '%Y-%m') as month,
            SUM(CASE WHEN type = 'debit' THEN amount ELSE 0 END) as total
        FROM transactions
        GROUP BY category, month
        ORDER BY category, month;
    """)

    rows = cursor.fetchall()
    conn.close()

    # Organize data
    data = {}
    for category, month, total in rows:
        if category not in data:
            data[category] = []
        data[category].append((month, float(total or 0)))

    result = []

    for category, values in data.items():
        if len(values) < 3:
            continue  # need enough history

        values.sort()

        current_month, current_val = values[-1]
        historical_vals = [v for (_, v) in values[:-1]]

        n = len(historical_vals)

        # -------- WEIGHTED MEAN --------
        weights = list(range(1, n + 1))  # increasing weights
        weighted_sum = sum(w * v for w, v in zip(weights, historical_vals))
        weight_total = sum(weights)

        weighted_mean = weighted_sum / weight_total

        # -------- WEIGHTED STD DEV --------
        variance = sum(
            w * ((v - weighted_mean) ** 2)
            for w, v in zip(weights, historical_vals)
        ) / weight_total

        weighted_std = math.sqrt(variance)

        if weighted_std == 0:
            continue

        # -------- Z-SCORE --------
        z_score = (current_val - weighted_mean) / weighted_std

        # -------- CLASSIFICATION --------
        if z_score > 2:
            status = "High Overspending"
        elif z_score > 1:
            status = "Above Normal"
        elif z_score < -1:
            status = "Reduced Spending"
        else:
            status = "Normal"

        result.append({
            "category": category,
            "current_month": current_val,
            "weighted_mean": round(weighted_mean, 2),
            "weighted_std": round(weighted_std, 2),
            "z_score": round(z_score, 2),
            "status": status
        })

    return result