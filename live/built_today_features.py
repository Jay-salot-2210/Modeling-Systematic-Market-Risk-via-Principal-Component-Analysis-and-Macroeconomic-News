import pandas as pd
import os

events = pd.read_csv("live_today_events_raw.csv")

daily = events.groupby("date").agg(
    total_events=("eventcode", "count"),
    mean_tone=("avgtone", "mean"),
    total_mentions=("nummentions", "sum")
).reset_index()

daily = daily.sort_values("date").iloc[-1:]
daily.to_csv("live_today_features.csv", index=False)

history_file = "live_features_history.csv"
if os.path.exists(history_file):
    daily.to_csv(history_file, mode="a", header=False, index=False)
else:
    daily.to_csv(history_file, index=False)

print("Live features updated")
print(daily)