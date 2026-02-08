import pandas as pd
import numpy as np
from sklearn.decomposition import PCA

returns = pd.read_csv('return_matrix.csv', index_col=0 )
sp500 = pd.read_csv('sp500.csv')

stock_used = returns.columns
sp500 = sp500[sp500['symbol'].isin(stock_used)]

X= (returns - returns.mean()) / returns.std()

pca = PCA()
pca.fit(X)

loadings = pd.DataFrame(
    pca.components_.T,
    index=stock_used,
    columns=[f'PC{i+1}' for i in range(pca.components_.shape[0])]
)

df = sp500.merge(loadings, left_on='symbol', right_index=True)

print(df.head())

sector_pc_means = (
    df.groupby("sector")[["PC2", "PC3", "PC4"]]
      .mean()
      .sort_values("PC2", ascending=False)
)

print(sector_pc_means)