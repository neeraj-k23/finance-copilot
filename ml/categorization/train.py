import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import pickle

# Load dataset
df = pd.read_csv("data/transactions.csv")

# Drop null narrations
df = df.dropna(subset=["narration"])

# -------- CREATE LABELS (IMPORTANT) --------
def assign_category(desc):
    desc = str(desc).lower()

    if "swiggy" in desc or "zomato" in desc:
        return "Food"
    elif "uber" in desc or "ola" in desc:
        return "Transport"
    elif "amazon" in desc or "flipkart" in desc:
        return "Shopping"
    elif "netflix" in desc or "spotify" in desc:
        return "Entertainment"
    elif "rent" in desc:
        return "Housing"
    elif "electricity" in desc or "bill" in desc:
        return "Utilities"
    else:
        return "Other"

df["category"] = df["narration"].apply(assign_category)

# -------- TRAIN MODEL --------
X = df["narration"]
y = df["category"]

vectorizer = TfidfVectorizer()
X_vec = vectorizer.fit_transform(X)

model = LogisticRegression(max_iter=200)
model.fit(X_vec, y)

# -------- SAVE --------
with open("ml/categorization/model.pkl", "wb") as f:
    pickle.dump(model, f)

with open("ml/categorization/vectorizer.pkl", "wb") as f:
    pickle.dump(vectorizer, f)

print("Model trained and saved!")
