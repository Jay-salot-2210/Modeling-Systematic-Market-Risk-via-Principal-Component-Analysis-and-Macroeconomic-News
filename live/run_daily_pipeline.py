import subprocess

print("Fetching live news...")
subprocess.run(["python", "live/fetch_today_news.py"], check=True)

print("Building features...")
subprocess.run(["python", "live/build_today_features.py"], check=True)

print("Predicting PC1...")
subprocess.run(["python", "live/predict_pc1_today.py"], check=True)

print("Daily PC1 pipeline completed")