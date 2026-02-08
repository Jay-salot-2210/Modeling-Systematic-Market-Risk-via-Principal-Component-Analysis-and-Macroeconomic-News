import pandas as pd 
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.metrics import roc_auc_score, f1_score, accuracy_score

df = pd.read_csv("events_pc1_dataset.csv", index_col=0, parse_dates=True)

X= df[["total_events", "mean_tone", "total_mentions"]]
y = df["PC1_Direction"]

split = int(0.8 * len(df))
X_train,X_test= X.iloc[:split], X.iloc[split:]
y_train,y_test= y.iloc[:split], y.iloc[split:]

models = {
    "Logisticregression":Pipeline([
        ("scaler", StandardScaler()),
        ("model", LogisticRegression(max_iter=1000))
    ]),
    "SVM_RBF":Pipeline([
        ("scaler", StandardScaler()),
        ("model", SVC(kernel='rbf', probability=True))
    ])
}

thresholds = np.arange(0.1, 0.9, 0.01)

results = []

for name, model in models.items():
    model.fit(X_train, y_train)
    y_prob = model.predict_proba(X_test)[:, 1]

    for t in thresholds:
        preds = (y_prob >= t).astype(int) *2 -1 
        acc = accuracy_score(y_test, preds)
        f1 = f1_score(y_test, preds)
        roc_auc = roc_auc_score(y_test, y_prob)

        results.append({
            "model": name,
            "threshold": t,
            "accuracy": acc,
            "f1_score": f1,
            "roc_auc": roc_auc
        })

results_df = pd.DataFrame(results)
best = results_df.sort_values("f1_score", ascending=False).head(10)

print("Top threshold configurations:")
print(best)