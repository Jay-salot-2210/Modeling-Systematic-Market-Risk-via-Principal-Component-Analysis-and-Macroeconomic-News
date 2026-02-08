import pandas as pd
import numpy as np
from sklearn.decomposition import PCA

returns = pd.read_csv('return_matrix.csv', index_col=0, parse_dates=True)

X = (returns - returns.mean()) / returns.std()
pca = PCA() 
pca.fit(X)

pc1_weights = pca.components_[0]
pc1_weights = pc1_weights/np.sum(np.abs(pc1_weights))

pc1_returns = returns @ pc1_weights
pc1_returns.name = 'PC1_Returns'

pc1_returns.to_csv('pc1_returns.csv')

print("Saved Pc1 returns to 'pc1_returns.csv'")

labels = pc1_returns.copy()
labels[labels > 0] = 1
labels[labels <= 0] = -1

labels=labels.astype(int)
labels.name = 'PC1_Direction'

labels.to_csv('pc1_labels.csv')
print(f"label distribution:\n{labels.value_counts()}")
