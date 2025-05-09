from flask import Flask, render_template, request
import os
import requests

app = Flask(__name__)

# Get YouTube API key from environment variable
YOUTUBE_API_KEY = os.environ.get("YOUTUBE_API_KEY")

def get_youtube_keywords(query):
    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "part": "snippet",
        "q": query,
        "type": "video",
        "maxResults": 50,
        "key": YOUTUBE_API_KEY,
    }

    response = requests.get(url, params=params)

    # DEBUG LOGGING: print the raw API response to Render logs
    print("YouTube API Response:", response.status_code, response.text)

    if response.status_code != 200:
        return []

    data = response.json()
    keywords = []

    for item in data.get("items", []):
        title = item["snippet"]["title"]
        score = min(100, len(title))  # Fake score logic (adjust if needed)
        keywords.append({"keyword": title, "score": score})

    return keywords

@app.route("/", methods=["GET", "POST"])
def index():
    keyword_data = []
    base_keyword = ""

    if request.method == "POST":
        base_keyword = request.form.get("keyword", "")
        if base_keyword:
            keyword_data = get_youtube_keywords(base_keyword)

    return render_template("index.html", keywords=keyword_data, base=base_keyword)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
