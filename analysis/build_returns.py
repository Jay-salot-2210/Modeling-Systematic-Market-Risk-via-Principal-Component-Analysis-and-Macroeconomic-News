import pandas as pd
import numpy as np

prices = pd.read_csv('all_prices.csv', index_col=0, parse_dates=True)

prices = prices.dropna(axis=1,thresh= 0.95*len(prices))

returns = np.log(prices / prices.shift(1)).dropna()

returns.to_csv('return_matrix.csv')

print("Returns matrix shape:", returns.shape)