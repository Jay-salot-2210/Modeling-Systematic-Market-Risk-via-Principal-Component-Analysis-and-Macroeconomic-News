import sys
import os
import pandas as pd
import joblib

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_ROOT)

from models.pc1_model_config import THRESHOLD, SIGN

df = pd.read_csv("live_today_features.csv")
date = df["date"].iloc[0]
X = df[["total_events", "mean_tone", "total_mentions"]]
MODEL_PATH = os.path.join(PROJECT_ROOT, "models", "pc1_event_model.pkl")
print("Loading model from:", MODEL_PATH)
model = joblib.load(MODEL_PATH)

proba = model.predict_proba(X)[0][1]
direction = SIGN if proba >= THRESHOLD else -SIGN
result = pd.DataFrame({
    "date": [date],
    "pc1_probability": [proba],
    "pc1_direction": [direction]
})

result.to_csv("live_predictions_log.csv", index=False)

print("Saved live_predictions_log.csv")