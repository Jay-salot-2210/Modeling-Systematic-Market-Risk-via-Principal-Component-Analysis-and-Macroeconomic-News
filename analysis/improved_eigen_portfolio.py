import pandas as pd
import numpy as np
from sklearn.decomposition import PCA

returns = pd.read_csv('return_matrix.csv', index_col=0, parse_dates=True)

X = (returns - returns.mean()) / returns.std()
pca = PCA() 
pca.fit(X)

results=[]

for i in range(3,10):
    k = i
    tail_components = pca.components_[-k:]

    weight = tail_components.mean(axis=0)
    weight = weight / np.sum(np.abs(weight))

    portfolio_returns = returns @ weight
    corr = portfolio_returns.corr(returns.mean(axis=1))
    results.append(
        {
            'k': k,
            'MarketCorrelation': corr,
            'AbsoluteCorrelation': abs(corr)
        }
    )

results_df = pd.DataFrame(results)
print("market correlation for tail PCA portfolios:")
print(results_df)

best_row = results_df.loc[results_df['AbsoluteCorrelation'].idxmin()]
best_k = int(best_row['k'])

print(f"\nBest k: {best_k} with Market Correlation: {best_row['MarketCorrelation']:.4f}")

results_df.to_csv('tail_pca_portfolio_market_correlation.csv', index=False)

