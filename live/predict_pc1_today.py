import pandas as pd
import joblib
from datetime import date
from models.pc1_model_config import THRESHOLD, SIGN

model = joblib.load("models/pc1_live_model.pkl")

X_today = pd.read_csv("live_today_features.csv")
X_today = X_today[["total_events", "mean_tone", "total_mentions"]]

prob = model.predict_proba(X_today)[:, 1][0]
signal = SIGN * (1 if prob >= THRESHOLD else -1)

out = pd.DataFrame([{
    "date": date.today(),
    "pc1_probability": prob,
    "pc1_direction": signal
}])

log_file = "live_predictions_log.csv"
if os.path.exists(log_file):
    out.to_csv(log_file, mode="a", header=False, index=False)
else:
    out.to_csv(log_file, index=False)

print(out)