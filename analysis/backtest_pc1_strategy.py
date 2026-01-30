import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression


events = pd.read_csv("events_pc1_dataset.csv", index_col=0, parse_dates=True)
pc1_returns = pd.read_csv("pc1_returns.csv", index_col=0, parse_dates=True)

X = events[["total_events", "mean_tone", "total_mentions"]]
y = events["PC1_Direction"]

split = int(0.8 * len(events))
X_train, X_test = X.iloc[:split], X.iloc[split:]
y_test = y.iloc[split:]

model = Pipeline([
    ("scaler", StandardScaler()),
    ("clf", LogisticRegression(max_iter=1000))
])

model.fit(X_train, y.iloc[:split])

probs = model.predict_proba(X_test)[:, 1]
signals = (probs > 0.55).astype(int) * 2 - 1

strategy_returns = (-signals) * pc1_returns.loc[X_test.index].values.squeeze()

print("Strategy mean return:", strategy_returns.mean())
print("Strategy volatility:", strategy_returns.std())
print("Sharpe (daily):", strategy_returns.mean() / strategy_returns.std())
print("Correlation with PC1:", np.corrcoef(strategy_returns, pc1_returns.loc[X_test.index].values.squeeze())[0,1])
