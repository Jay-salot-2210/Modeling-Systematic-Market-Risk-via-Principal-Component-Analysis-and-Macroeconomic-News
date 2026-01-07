import requests
import zipfile
import io
import pandas as pd
from datetime import datetime,timedelta
from tqdm import tqdm

START_DATE = datetime(2010, 1, 4)
END_DATE   = datetime(2025, 12, 29)

def daterange(start,end):
    for n in range((end-start).days+1):
        yield start+timedelta(n)

rows = []

for date in tqdm(list(daterange(START_DATE, END_DATE))):
    datestr = date.strftime("%Y%m%d")
    url = f"http://data.gdeltproject.org/events/{datestr}.export.CSV.zip"

    try:
        r = requests.get(url, timeout=30)
        if r.status_code != 200:
            continue

        with zipfile.ZipFile(io.BytesIO(r.content)) as z:
            with z.open(z.namelist()[0]) as f:
                df = pd.read_csv(
                    f,
                    sep="\t",
                    header=None,
                    usecols=[0, 26, 27, 30],
                    names=["event_date", "event_code", "avg_tone", "num_mentions"],
                    low_memory=False
                )
                df["date"] = date.date()
                rows.append(df)

        print("Downloaded", datestr)

    except Exception:
        print("Skipped", datestr)

events = pd.concat(rows, ignore_index=True)
events.to_csv("gdelt_events_raw.csv", index=False)

print("Saved gdelt_events_raw.csv")