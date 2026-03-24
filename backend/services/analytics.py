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
        if len(values) < 2:
            continue

        # Sort by month
        values.sort()

        current_month, current_val = values[-1]
        prev_month, prev_val = values[-2]

        # Historical average (excluding current)
        historical_vals = [v for (_, v) in values[:-1]]
        avg = sum(historical_vals) / len(historical_vals) if historical_vals else 0

        # Avoid division by zero
        prev_change = ((current_val - prev_val) / prev_val * 100) if prev_val != 0 else 0
        avg_change = ((current_val - avg) / avg * 100) if avg != 0 else 0

        # Decision logic
        status = "Normal"

        if prev_change > 30 and avg_change > 30:
            status = "High Overspending"
        elif prev_change > 30:
            status = "Recent Spike"
        elif avg_change > 30:
            status = "Above Average"
        elif prev_change < -30 and avg_change < -30:
            status = "Reduced Spending"

        result.append({
            "category": category,
            "current_month": current_val,
            "previous_month": prev_val,
            "historical_avg": round(avg, 2),
            "prev_change_percent": round(prev_change, 2),
            "avg_change_percent": round(avg_change, 2),
            "status": status
        })

    return result