import requests

URL = "https://api.gdeltproject.org/api/v2/doc/doc"
params = {
    "query": "(economy OR inflation OR \"interest rates\")",
    "mode": "ArtList",
    "maxrecords": 10,
    "format": "json"
}

print(f"Requesting {URL} with params: {params}")

try:
    r = requests.get(URL, params=params, timeout=15)
    print(f"Status Code: {r.status_code}")
    print(f"Headers: {r.headers}")
    data = r.json()
    articles = data.get("articles", [])
    if articles:
        print(f"Article Keys: {list(articles[0].keys())}")
    else:
        print("No articles found.")
except Exception as e:
    print(f"Error: {e}")
