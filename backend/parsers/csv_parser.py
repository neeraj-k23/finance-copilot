import pandas as pd

def parse_csv(file_path):
    df = pd.read_csv(file_path)

    # Adjust based on dataset columns
    df = df.rename(columns={
        "Date": "date",
        "Description": "description",
        "Debit": "debit",
        "Credit": "credit",
        "Balance": "balance"
    })

    df["amount"] = df["debit"].fillna(0) * -1 + df["credit"].fillna(0)
    df["type"] = df["amount"].apply(lambda x: "debit" if x < 0 else "credit")

    df = df[["date", "description", "amount", "type", "balance"]]

    return df

