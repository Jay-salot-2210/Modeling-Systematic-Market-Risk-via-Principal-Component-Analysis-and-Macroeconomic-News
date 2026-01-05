import pandas as pd
import numpy as np  
from sklearn.decomposition import PCA

returns = pd.read_csv('return_matrix.csv', index_col=0, parse_dates=True)

X = (returns - returns.mean()) / returns.std()
pca = PCA()
pca.fit(X)

pc1_weights = pca.components_[0]
pc1_weights = pc1_weights / np.sum(np.abs(pc1_weights))

pc1_returns = returns @ pc1_weights
pc1_returns.name = 'PC1'

sp500_index = pd.read_csv('all_prices.csv', index_col=0, parse_dates=True)

if "^GSPC" in sp500_index.columns:
    market_prices = sp500_index["^GSPC"]
else:
    market_prices = sp500_index.mean(axis=1)

market_returns = np.log(market_prices / market_prices.shift(1)).dropna()
market_returns.name = 'Market'

df=pd.concat([pc1_returns, market_returns], axis=1).dropna()

print(df.head())

corr = df["PC1"].corr(df["Market"])
print(f"\nCorrelation between PC1 and Market: {corr:.4f}")

import matplotlib.pyplot as plt

plt.figure(figsize=(10,5))
plt.plot(df.index, df["PC1"].cumsum(), label="PC1 Portfolio")
plt.plot(df.index, df["Market"].cumsum(), label="Market Index")
plt.legend()
plt.title("PC1 vs Market Cumulative Returns")
plt.xlabel("Date")
plt.ylabel("Cumulative Log Returns")
plt.show()
