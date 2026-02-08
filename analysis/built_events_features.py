import pandas as pd

print("Starting chunked processing of GDELT events...")

chunk_size = 1_000_000  
daily_agg = {}

for i, chunk in enumerate(
    pd.read_csv(
        "gdelt_events_raw.csv",
        chunksize=chunk_size,
        low_memory=False
    ),
    start=1
):
    print(f"Processing chunk {i}...")
    chunk["avg_tone"] = pd.to_numeric(chunk["avg_tone"], errors="coerce")

    grouped = chunk.groupby("date").agg(
        total_events=("event_code", "count"),
        mean_tone=("avg_tone", "mean"),
        total_mentions=("num_mentions", "sum")
    )

    for date, row in grouped.iterrows():
        if date not in daily_agg:
            daily_agg[date] = {
                "total_events": 0,
                "tone_sum": 0.0,
                "tone_count": 0,
                "total_mentions": 0
            }

        daily_agg[date]["total_events"] += row["total_events"]
        daily_agg[date]["total_mentions"] += row["total_mentions"]

        if not pd.isna(row["mean_tone"]):
            daily_agg[date]["tone_sum"] += row["mean_tone"]
            daily_agg[date]["tone_count"] += 1

print("Finalizing daily aggregates...")

rows = []
for date, stats in daily_agg.items():
    mean_tone = (
        stats["tone_sum"] / stats["tone_count"]
        if stats["tone_count"] > 0 else 0
    )
    rows.append([
        date,
        stats["total_events"],
        mean_tone,
        stats["total_mentions"]
    ])

daily = pd.DataFrame(
    rows,
    columns=["date", "total_events", "mean_tone", "total_mentions"]
)

daily = daily.sort_values("date")
daily.to_csv("daily_event_features.csv", index=False)

print("Saved daily_event_features.csv successfully")
print(daily.head())
