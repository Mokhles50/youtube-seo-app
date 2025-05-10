from flask import Flask, render_template, request
import requests
from pytrends.request import TrendReq
from bs4 import BeautifulSoup

app = Flask(__name__)

YOUTUBE_API_KEY = "AIzaSyDB3uRLRelUIy_4K3Im2NOGKDWzTbb7bCc"

def fetch_youtube_keywords(query):
    url = f"https://suggestqueries.google.com/complete/search?client=firefox&ds=yt&q={query}"
    response = requests.get(url)
    suggestions = response.json()[1]
    return suggestions[:50]  # Top 50 suggestions

def estimate_search_volume(keyword):
    # Dummy logic — can be replaced with real data
    return len(keyword) * 1000

def estimate_difficulty(keyword):
    search_url = f"https://www.youtube.com/results?search_query={keyword}"
    response = requests.get(search_url)
    soup = BeautifulSoup(response.text, "html.parser")
    results_count = len(soup.find_all("a"))
    score = min(max((results_count / 100), 1), 100)
    return round(score, 2)

def is_trending(keyword):
    pytrends = TrendReq()
    try:
        pytrends.build_payload([keyword], timeframe='now 7-d')
        data = pytrends.interest_over_time()
        if not data.empty:
            return data[keyword].iloc[-1] > data[keyword].iloc[0]
    except:
        return False
    return False

@app.route("/", methods=["GET", "POST"])
def index():
    results = []
    if request.method == "POST":
        keyword = request.form["keyword"]
        suggestions = fetch_youtube_keywords(keyword)
        for suggestion in suggestions:
            volume = estimate_search_volume(suggestion)
            difficulty = estimate_difficulty(suggestion)
            trending = is_trending(suggestion)
            results.append({
                "keyword": suggestion,
                "volume": volume,
                "difficulty": difficulty,
                "trending": trending
            })
        results.sort(key=lambda x: x["difficulty"])  # Default sort
    return render_template("index.html", results=results)

@app.route("/blog/best-tool")
def blog_best_tool():
    return render_template("blog/best-tool.html")

if __name__ == "__main__":
    app.run(debug=True)
 
