import pandas as pd

events = pd.read_csv("live_today_events_raw.csv", parse_dates=["Date"])

daily = events.groupby("Date").agg(
    total_events=("GLOBALEVENTID", "count"),
    mean_tone=("AvgTone", "mean"),
    total_mentions=("NumMentions", "sum")
).reset_index()

daily = daily.sort_values("Date").iloc[-1:]

daily.to_csv("live_today_features.csv", index=False)
print("saved live today features.csv ")
print(daily)