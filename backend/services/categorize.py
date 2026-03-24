import pickle

with open("ml/categorization/model.pkl", "rb") as f:
    model = pickle.load(f)

with open("ml/categorization/vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)

def rule_based_category(desc):
    desc = str(desc).lower()

    if "gas" in desc or "petrol" in desc or "fuel" in desc:
        return "Fuel"
    elif "atm" in desc:
        return "Cash Withdrawal"
    elif "upi" in desc:
        return "Transfer"

    return None

def predict_category(description: str) -> str:
    # Rule-based first
    rule = rule_based_category(description)
    if rule:
        return rule

    # ML fallback
    X = vectorizer.transform([description])
    return model.predict(X)[0]