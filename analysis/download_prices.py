import yfinance as yf
import pandas as pd
from eigenprotfolio.preprocessor_tickers import get_cleaned_tickers


tickers = get_cleaned_tickers()

data = yf.download(
    tickers,
    start = "2010-01-01",
    progress= True,
    auto_adjust= True,
)

prices= data["Close"]
prices.to_csv("all_prices.csv")

print("Saved prices.csv with shape:", prices.shape)