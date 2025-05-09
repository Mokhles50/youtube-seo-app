# app.py
from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")  # Secure method for Render


def get_youtube_keywords(query):
    search_url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "part": "snippet",
        "maxResults": 50,
        "q": query,
        "type": "video",
        "key": YOUTUBE_API_KEY
    }
    response = requests.get(search_url, params=params)
    results = []

    if response.status_code == 200:
        data = response.json()
        for item in data.get("items", []):
            title = item["snippet"]["title"]
            description = item["snippet"]["description"]
            results.append({
                "title": title,
                "description": description
            })

    # Simple keyword frequency analysis from titles
    keyword_freq = {}
    for result in results:
        words = result["title"].lower().split()
        for word in words:
            if len(word) > 3:  # Filter short/common words
                keyword_freq[word] = keyword_freq.get(word, 0) + 1

    sorted_keywords = sorted(keyword_freq.items(), key=lambda x: x[1], reverse=True)

    return [{"keyword": kw, "score": freq} for kw, freq in sorted_keywords[:50]]


@app.route("/", methods=["GET", "POST"])
def index():
    keyword_data = []
    base_keyword = ""
    if request.method == "POST":
        base_keyword = request.form.get("keyword")
        keyword_data = get_youtube_keywords(base_keyword)
    return render_template("index.html", keywords=keyword_data, base=base_keyword)


if __name__ == "__main__":
    app.run(debug=True)
