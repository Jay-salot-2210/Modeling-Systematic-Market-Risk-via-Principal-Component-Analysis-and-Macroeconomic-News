import pandas as pd
import joblib
from models.pc1_model_config import build_model

df = pd.read_csv(
    "events_pc1_dataset.csv",
    index_col=0,
    parse_dates=True
)

last_train_date = df.index.max() - pd.offsets.MonthEnd(1)
train_df = df.loc[:last_train_date]

print("Retraining using data up to:", last_train_date.date())
print("Training samples:", len(train_df))

X = train_df[["total_events", "mean_tone", "total_mentions"]]
y = train_df["PC1_Direction"]

model = build_model()
model.fit(X, y)

joblib.dump(model, "models/pc1_live_model.pkl")

print(" Model retrained and updated")
