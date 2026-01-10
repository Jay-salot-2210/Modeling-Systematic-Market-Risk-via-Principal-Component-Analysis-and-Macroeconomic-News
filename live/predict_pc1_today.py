import pandas as pd
import joblib
from models.pc1_model_config import THRESHOLD,SIGN

model = joblib.load("models/pc1_event_model.pkl")

X_today = pd.read_csv("live_today_features.csv")
X_today = X_today[["total_events", "mean_tone", "total_mentions"]]

prob = model.predict_proba(X_today)[:, 1][0]

signal = SIGN * (1 if prob > THRESHOLD else -1)

print(f"PC1 Probability : {prob:.4f}")
print(f"Predicted PC1 Direction : {signal}")