import subprocess

print("Fetching live news and building features...")
subprocess.run(["python", "live/fetch_today_news.py"], check=True)

print("Predicting PC1...")
subprocess.run(["python", "live/predict_pc1_today.py"], check=True)

print("Explaining prediction...")
subprocess.run(["python", "analysis/explain_pc1_today.py"], check=True)

print("Daily PC1 pipeline completed")