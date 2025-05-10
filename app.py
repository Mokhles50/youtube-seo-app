from flask import Flask, render_template, request
import requests
import os
from pytrends.request import TrendReq
import random

app = Flask(__name__)

YOUTUBE_API_KEY = 'AIzaSyDB3uRLRelUIy_4K3Im2NOGKDWzTbb7bCc'

# Function to get YouTube keyword suggestions (expanded with variations)
def get_youtube_keywords(query):
    suggestions = set()

    # Main keyword
    suggest_url = f'https://suggestqueries.google.com/complete/search?client=firefox&ds=yt&q={query}'
    res = requests.get(suggest_url)
    if res.status_code == 200:
        suggestions.update(res.json()[1])

    # Expanded suggestions (a–z)
    for char in 'abcdefghijklmnopqrstuvwxyz':
        res = requests.get(f'https://suggestqueries.google.com/complete/search?client=firefox&ds=yt&q={query} {char}')
        if res.status_code == 200:
            suggestions.update(res.json()[1])
        if len(suggestions) >= 50:
            break

    return list(suggestions)[:50]

# Simulated function to estimate search volume (replace with real data source if needed)
def estimate_search_volume(keyword):
    return random.randint(1000, 500000)

# Estimate difficulty based on video count
def estimate_difficulty(keyword):
    search_url = f'https://www.googleapis.com/youtube/v3/search?part=snippet&q={keyword}&type=video&key={YOUTUBE_API_KEY}'
    res = requests.get(search_url)
    items = res.json().get('items', [])
    count = len(items)
    difficulty = min(100, int((count / 50) * 100))  # 0–100 scale
    return difficulty

# Check trending status using Google Trends
def is_trending(keyword):
    try:
        pytrends = TrendReq(hl='en-US', tz=360)
        pytrends.build_payload([keyword], cat=0, timeframe='now 7-d', geo='', gprop='youtube')
        data = pytrends.interest_over_time()
        if not data.empty:
            trend = data[keyword].iloc[-1]
            return "Yes" if trend > data[keyword].mean() else "No"
        return "No"
    except:
        return "No"

@app.route("/", methods=["GET", "POST"])
def index():
    keyword_data = []
    base_keyword = ""

    if request.method == "POST":
        base_keyword = request.form["keyword"]
        keywords = get_youtube_keywords(base_keyword)

        for kw in keywords:
            volume = estimate_search_volume(kw)
            difficulty = estimate_difficulty(kw)
            trending = is_trending(kw)

            keyword_data.append({
                "keyword": kw,
                "volume": volume,
                "difficulty": difficulty,
                "trending": trending
            })

    return render_template("index.html", keywords=keyword_data, base=base_keyword)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(debug=True, host="0.0.0.0", port=port)
    @app.route("/blog/best-tool")
def blog_best_tool():
    return render_template("blog/best-tool.html")
    @app.route("/blog/best-tool")
def blog_best_tool():
    return render_template("blog/best-tool.html")


