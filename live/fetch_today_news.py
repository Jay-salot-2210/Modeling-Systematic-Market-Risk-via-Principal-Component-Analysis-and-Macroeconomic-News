import requests
import pandas as pd
from datetime import date

Today = date.today().strftime("%Y-%m-%d")

url = (
    "https://api.gdeltproject.org/api/v2/events/search"
    "?query=economy OR inflation OR interest rate OR central bank"
    "&maxrecords=300"
    "&format=json"
)

r = requests.get(url)
data = r.json().get("events", [])

df = pd.DataFrame(data)

if df.empty:
    raise ValueError("No events fetched from GDELT API.")

df["Date"] = pd.to_datetime(df["day"])

df.to_csv("live_today_events_raw.csv", index=False)
print("Saved Live Today's raw events csv.")