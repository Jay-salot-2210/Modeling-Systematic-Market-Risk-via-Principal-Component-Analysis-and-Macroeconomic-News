import pandas as pd

def get_cleaned_tickers(csv_path = "nifty50.csv"):
    df = pd.read_csv(csv_path)
    tickers = df["symbol"].tolist()
    return tickers

if __name__ == "__main__":
    tickers = get_cleaned_tickers()
    print(f"Total tickers fetched: {len(tickers)}")
    print(tickers)
