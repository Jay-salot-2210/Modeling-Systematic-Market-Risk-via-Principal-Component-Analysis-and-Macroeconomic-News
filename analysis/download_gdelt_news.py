import requests
import zipfile
import io
import pandas as pd
from datetime import datetime

START_DATE = datetime(2019, 1, 1)
END_DATE   = datetime(2020, 12, 31)

MASTER_URL = "http://data.gdeltproject.org/gdeltv2/masterfilelist.txt"

print("Downloading master file list...")
master = requests.get(MASTER_URL).text.splitlines()

rows = []

for line in master:
    if "mentions.CSV.zip" not in line:
        continue

    parts = line.split(" ")
    url = parts[2]

    # Extract datetime from filename
    filename = url.split("/")[-1]
    datestr = filename.split(".")[0]  # YYYYMMDDHHMMSS
    file_date = datetime.strptime(datestr, "%Y%m%d%H%M%S")

    if not (START_DATE <= file_date <= END_DATE):
        continue

    try:
        r = requests.get(url, timeout=60)
        with zipfile.ZipFile(io.BytesIO(r.content)) as z:
            with z.open(z.namelist()[0]) as f:
                df = pd.read_csv(
                    f,
                    sep="\t",
                    header=None,
                    usecols=[1, 5],
                    names=["date", "headline"],
                    encoding="latin1",
                    low_memory=False
                )

                df["date"] = file_date.date()
                rows.append(df)

        print("Downloaded", filename)

    except Exception:
        print("Failed", filename)

news_raw = pd.concat(rows, ignore_index=True)
news_raw.to_csv("news_raw.csv", index=False)

print("Saved news_raw.csv")
