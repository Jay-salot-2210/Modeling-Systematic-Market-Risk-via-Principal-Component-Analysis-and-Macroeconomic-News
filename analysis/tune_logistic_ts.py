import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import roc_auc_score
import numpy as np

df = pd.read_csv("events_pc1_dataset.csv", index_col=0, parse_dates=True)

X = df[["total_events", "mean_tone", "total_mentions"]]
y = df["PC1_Direction"]

tscv = TimeSeriesSplit(n_splits=5)
Cs = [0.01, 0.1, 1, 5, 10]

results = []

for C in Cs:
    aucs = []
    for train_idx, test_idx in tscv.split(X):
        model = Pipeline([
            ("scaler", StandardScaler()),
            ("clf", LogisticRegression(C=C, max_iter=1000))
        ])
        model.fit(X.iloc[train_idx], y.iloc[train_idx])
        probs = model.predict_proba(X.iloc[test_idx])[:, 1]
        aucs.append(roc_auc_score(y.iloc[test_idx], probs))

    results.append({"C": C, "Mean_AUC": np.mean(aucs)})

res_df = pd.DataFrame(results)
print(res_df.sort_values("Mean_AUC", ascending=False))
