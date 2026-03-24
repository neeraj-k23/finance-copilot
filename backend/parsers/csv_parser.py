import pandas as pd

def parse_csv(file_path):
    df = pd.read_csv(file_path)

    # Rename based on YOUR dataset
    df = df.rename(columns={
        "narration": "description",
        "transactionTimestamp": "date",
        "currentBalance": "balance",
        "type": "type",
        "amount": "amount"
    })

    # -------- CLEAN DATA --------

    # Handle null descriptions
    df["description"] = df["description"].fillna("unknown")

    # Convert date to proper format
    df["date"] = pd.to_datetime(df["date"], errors="coerce").dt.date

    # Convert amount to float
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")

    # Convert type
    df["type"] = df["type"].apply(lambda x: "debit" if str(x).upper() == "DEBIT" else "credit")

    # Drop rows with invalid data
    df = df.dropna(subset=["date", "amount"])

    # Select final columns
    df = df[["date", "description", "amount", "type", "balance"]]

    return df