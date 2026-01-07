import pandas as pd

events = pd.read_csv("daily_event_features.csv",parse_dates=["date"])
print(f"Events rows : {len(events)}")

labels = pd.read_csv("pc1_labels.csv",index_col=0,parse_dates=True)
print(f"PC1 labels rows : {len(labels)}")
print("Shifting PC1 labels (predict next day) ")
labels = labels.shift(-1)

print("Aligning dataset")
dataset = events.set_index("date").join(labels, how="inner")
dataset = dataset.dropna()

print(f"Final alligned dataset size : {dataset.shape}")

dataset.to_csv("events_pc1_dataset.csv")
print("Saved to csv")
print(dataset.head())