from backend.parsers.csv_parser import parse_csv
from backend.models.db import get_connection

def ingest_transactions(file_path):
    df = parse_csv(file_path)

    conn = get_connection()
    cursor = conn.cursor()

    for _, row in df.iterrows():
        cursor.execute("""
            INSERT INTO transactions (date, description, amount, type, balance)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            row["date"],
            row["description"],
            float(row["amount"]),
            row["type"],
            row["balance"]
        ))

    conn.commit()
    conn.close()

    return {"status": "success", "rows_inserted": len(df)}
