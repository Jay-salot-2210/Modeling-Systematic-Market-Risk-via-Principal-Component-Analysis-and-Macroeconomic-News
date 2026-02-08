import pandas as pd
import numpy as np
from sklearn.decomposition import PCA

returns = pd.read_csv('return_matrix.csv', index_col=0)

X = (returns - returns.mean()) / returns.std()

pca = PCA()
pca.fit(X)
explained_variance = pca.explained_variance_ratio_

print("Top 10 explained variance ratios:")
for i,v in enumerate(explained_variance[:10]):
    print(f"Component {i+1}: {v:.4f}")