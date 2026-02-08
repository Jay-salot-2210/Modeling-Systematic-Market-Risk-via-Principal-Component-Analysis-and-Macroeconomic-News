import pandas as pd
import joblib
import os
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

MODEL_PATH = "models/pc1_event_model.pkl"

print("Loading model for explanation...")
model = joblib.load(MODEL_PATH)

features = pd.read_csv("live_today_features.csv")
X = features[["total_events", "mean_tone", "total_mentions"]]

scaler = None
clf = None

for step in model.named_steps.values():
    if isinstance(step, StandardScaler):
        scaler = step
    if isinstance(step, LogisticRegression):
        clf = step

if scaler is None or clf is None:
    raise RuntimeError("Required model components not found for explanation.")

X_scaled = scaler.transform(X)

contributions = clf.coef_[0] * X_scaled[0]

explanation = pd.DataFrame({
    "feature": X.columns,
    "coefficient": clf.coef_[0],
    "value": X.iloc[0].values,
    "contribution": contributions
}).sort_values(by="contribution", key=np.abs, ascending=False)

explanation.to_csv("pc1_feature_explanation_today.csv", index=False)

print("Saved pc1_feature_explanation_today.csv")
print(explanation)

dashboard_path = "data/daily_pc1_dashboard.csv"

row = explanation.copy()
row["date"] = features["date"].iloc[0]
row["pc1_probability"] = joblib.load(MODEL_PATH).predict_proba(X)[0][1]

if not os.path.exists("data"):
    os.makedirs("data")

if os.path.exists(dashboard_path):
    existing = pd.read_csv(dashboard_path)
    updated = pd.concat([existing, row], ignore_index=True)
    # Deduplicate: Keep only the latest entry for each date + feature combo
    updated = updated.drop_duplicates(subset=["date", "feature"], keep="last")
else:
    updated = row

updated.to_csv(dashboard_path, index=False)
print("Updated daily_pc1_dashboard.csv (with deduplication)")