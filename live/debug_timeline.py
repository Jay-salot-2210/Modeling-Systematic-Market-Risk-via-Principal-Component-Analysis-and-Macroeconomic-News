import requests
import pandas as pd

URL = "https://api.gdeltproject.org/api/v2/doc/doc"
query = "(economy OR inflation OR \"interest rates\")"

def check_timeline(mode):
    params = {
        "query": query,
        "mode": mode,
        "format": "json"
    }
    print(f"Checking {mode}...")
    try:
        r = requests.get(URL, params=params, timeout=15)
        r.raise_for_status()
        data = r.json()
        print(f"Keys: {data.keys()}")
        if "timeline" in data:
            print(f"First point: {data['timeline'][0]}")
            print(f"Last point: {data['timeline'][-1]}")
    except Exception as e:
        print(f"Error: {e}")

check_timeline("TimelineVol")
check_timeline("TimelineTone")
