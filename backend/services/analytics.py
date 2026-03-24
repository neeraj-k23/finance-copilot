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