import pandas as pd
import numpy as np
from sklearn.decomposition import PCA

returns = pd.read_csv('return_matrix.csv', index_col=0, parse_dates=True)
window = 252*3
rebalance_freq = 21
k =  3

portfolio_returns = []

for i in range(window, len(returns), rebalance_freq):
    train = returns.iloc[i-window:i]
    
    X_train = (train - train.mean()) / train.std()
    pca = PCA() 
    pca.fit(X_train)

    tail_components = pca.components_[-k:]
    weight = tail_components.mean(axis=0)
    weight = weight / np.sum(np.abs(weight))
    
    test_period = returns.iloc[i:i+rebalance_freq]
    ret = test_period @ weight
    portfolio_returns.append(ret)

portfolio_returns = pd.concat(portfolio_returns)
portfolio_returns.name = 'Rolling_eigenportfolio'

portfolio_returns.to_csv('rolling_tail_pca_portfolio_returns.csv')

print(f"\n Mean daily return{portfolio_returns.mean():.6f}, \n Daily volatility: {portfolio_returns.std():.6f}, \n Market Correlation: {portfolio_returns.corr(returns.mean(axis=1)):.4f}")

