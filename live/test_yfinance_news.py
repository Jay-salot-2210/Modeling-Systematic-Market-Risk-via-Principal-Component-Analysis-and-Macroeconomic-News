import yfinance as yf
import pandas as pd

def get_yahoo_news(tickers = ["^NSEI", "RELIANCE.NS", "HDFCBANK.NS"]):
    all_news = []
    for ticker in tickers:
        try:
            t = yf.Ticker(ticker)
            news = t.news
            if news:
                print(f"Found {len(news)} articles for {ticker}")
                for article in news:
                    all_news.append({
                        "title": article.get("title", ""),
                        "provider": article.get("publisher", ""),
                        "link": article.get("link", ""),
                        "date": article.get("providerPublishTime", 0)
                    })
        except Exception as e:
            print(f"Error for {ticker}: {e}")
            
    print(f"Total articles found: {len(all_news)}")
    if len(all_news) > 0:
        print("Sample article:", all_news[0]['title'])
        
    return all_news

if __name__ == "__main__":
    get_yahoo_news()
