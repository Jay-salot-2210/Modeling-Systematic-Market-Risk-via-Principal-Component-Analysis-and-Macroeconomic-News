import pandas as pd
import requests
from datetime import datetime
import time
import logging
import os

if not os.path.exists("logs"):
    os.makedirs("logs")

logging.basicConfig(
    filename="logs/debug.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filemode="w"  # Overwrite each run
)

today = datetime.utcnow().strftime("%Y-%m-%d")
URL = "https://api.gdeltproject.org/api/v2/doc/doc"
QUERY = '(India OR NIFTY OR Sensex) (economy OR inflation OR GDP)'

def fetch_gdelt_metric(mode):
    params = {
        "query": QUERY,
        "mode": mode,
        "format": "json"
    }
    
    logging.info(f"Requesting {mode} with params: {params}")
    
    for attempt in range(3): # Retry loop
        try:
            r = requests.get(URL, params=params, timeout=30)
            if r.status_code != 200:
                logging.error(f"HTTP Error {r.status_code}: {r.text[:500]}")
                time.sleep(1)
                continue
                
            try:
                data = r.json()
            except ValueError:
                logging.error(f"JSON Decode Error. Text snippet: {r.text[:200]}")
                time.sleep(1)
                continue
            
            if "timeline" in data:
                timeline = data["timeline"]
                logging.info(f"Timeline length: {len(timeline)} for {mode}")
                
                points = timeline
                # Handle nested structure (e.g. [{'series':..., 'data': [...]}])
                if len(timeline) > 0 and isinstance(timeline[0], dict) and "data" in timeline[0]:
                    logging.info(f"Detected nested structure for {mode}")
                    points = timeline[0]["data"]
                
                if len(points) > 0:
                    # Check directly last point
                    last_point = points[-1]
                    if "value" in last_point and last_point["value"] is not None:
                        logging.info(f"Found valid value (last): {last_point['value']}")
                        return last_point["value"]
                    
                    # Search backwards
                    for i, point in enumerate(reversed(points)):
                        if "value" in point and point["value"] is not None:
                             logging.info(f"Found valid value (backwards at -{i}): {point['value']}")
                             return point["value"]
                
                logging.warning(f"Timeline empty or no valid values found for {mode}")
                return None # Don't retry if valid JSON but empty
            else:
                logging.error(f"No 'timeline' key in response for {mode}. Keys: {list(data.keys())}")
                return None
                
        except Exception as e:
            logging.error(f"Failed to fetch {mode} (attempt {attempt+1}): {e}", exc_info=True)
            time.sleep(1)
            
    return None

print("Fetching live news features from GDELT Timeline...")

# Fetch raw metrics
vol_intensity = fetch_gdelt_metric("TimelineVol")
time.sleep(1) # Be nice to API
avg_tone = fetch_gdelt_metric("TimelineTone")

import yfinance as yf

def fetch_yahoo_sentiment():
    """
    Fallback: Scrapes news from Yahoo Finance for NIFTY 50 and top constituents,
    calculates sentiment using a simple dictionary approach.
    """
    tickers = ["^NSEI", "RELIANCE.NS", "HDFCBANK.NS", "INFY.NS", "ICICIBANK.NS"]
    all_headlines = []
    
    print(f"Attempting Yahoo Finance fallback for: {tickers}")
    
    for t in tickers:
        try:
            ticker = yf.Ticker(t)
            news = ticker.news
            if news:
                print(f"  - {t}: Found {len(news)} articles")
                for n in news:
                    title = n.get("title", "")
                    if title:
                        all_headlines.append(title.lower())
            else:
                print(f"  - {t}: No news found")
        except Exception as e:
            print(f"  - {t}: Error {e}")
            logging.error(f"Yahoo fetch error for {t}: {e}")

    if not all_headlines:
        return 0.75, -2.0  # Absolute fallback if Yahoo also fails

    # Dictionary-based sentiment
    pos_words = {"growth", "surge", "rise", "gain", "bull", "jump", "rally", "profit", "high", "record", "strong", "recovery", "boost", "up", "positive"}
    neg_words = {"drop", "fall", "decline", "bear", "crash", "loss", "weak", "recession", "inflation", "risk", "fear", "slump", "down", "crisis", "negative", "warn"}

    total_score = 0
    total_words = 0

    for h in all_headlines:
        words = h.split()
        score = 0
        for w in words:
            w_clean = w.strip('.,:;!?')
            if w_clean in pos_words:
                score += 1
            elif w_clean in neg_words:
                score -= 1
        
        # TimelineTone is roughly % difference (Pos - Neg)
        # We approximate this by (Score / WordCount) * 100
        # Typical headline has ~10-15 words.
        # If 1 pos word in 10 words -> 10%
        if len(words) > 0:
            total_score += (score / len(words)) * 100
    
    avg_tone = total_score / len(all_headlines) if all_headlines else 0
    
    # Volume intensity proxy: normalize article count (e.g., 50 articles = 1.0)
    vol_intensity = min(len(all_headlines) / 50.0, 1.0)
    if vol_intensity < 0.2: vol_intensity = 0.2 # Floor
    
    print(f"Yahoo Fallback: Found {len(all_headlines)} articles. Tone: {avg_tone:.2f}, Vol: {vol_intensity:.2f}")
    return vol_intensity, avg_tone

# Fallbacks
if vol_intensity is None or avg_tone is None:
    print("[WARNING] GDELT fetch failed, switching to Yahoo Finance fallback...")
    logging.warning("Switching to Yahoo Finance fallback")
    vol_intensity, avg_tone = fetch_yahoo_sentiment()

# Scale values
total_events = vol_intensity * 200000
mean_tone = avg_tone + 72.0
total_mentions = total_events * 0.5

print(f"Fetched: Vol={vol_intensity}, Tone={avg_tone}")
print(f"Scaled: Events={total_events}, Tone={mean_tone}, Mentions={total_mentions}")

features = pd.DataFrame([{
    "date": today,
    "total_events": total_events,
    "mean_tone": mean_tone,
    "total_mentions": total_mentions
}])

features.to_csv("live_today_features.csv", index=False)
print("Saved live_today_features.csv")