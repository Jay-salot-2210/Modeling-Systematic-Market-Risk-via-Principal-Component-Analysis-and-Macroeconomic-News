import pandas as pd
import joblib
from models.pc1_model_config import build_model

df = pd.read_csv("events_pc1_dataset.csv", index_col=0, parse_dates=True)

X = df[["total_events", "mean_tone", "total_mentions"]]
y = df["PC1_Direction"]

split = int(0.8 * len(df))
X_train= X.iloc[:split]
y_train = y.iloc[:split]

model = build_model()
model.fit(X_train, y_train)

joblib.dump(model, "models/pc1_event_model.pkl")
print("PC1 model trained and saved")