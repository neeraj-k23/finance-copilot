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
