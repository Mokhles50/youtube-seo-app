from flask import Flask, render_template, request
from pytrends.request import TrendReq
from googleapiclient.discovery import build
import requests
import random

app = Flask(__name__)

# Your YouTube API Key
YOUTUBE_API_KEY = "AIzaSyDB3uRLRelUIy_4K3Im2NOGKDWzTbb7bCc"

# Initialize YouTube and Google Trends clients
youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
pytrends = TrendReq(hl='en-US', tz=360)

def get_youtube_keywords(query):
    suggest_url = f'https://suggestqueries.google.com/complete/search?client=firefox&ds=yt&q={query}'
    res = requests.get(suggest_url)
    suggestions = res.json()[1] if res.status_code == 200 else []
    return suggestions[:50]

def get_search_volume(keyword):
    return random.randint(1000, 100000)  # Placeholder unless you integrate a real service

def is_trending(keyword):
    try:
        pytrends.build_payload([keyword], cat=0, timeframe='now 7-d', geo='', gprop='youtube')
        data = pytrends.interest_over_time()
        if not data.empty and data[keyword].iloc[-1] > data[keyword].mean():
            return "Yes"
    except:
        pass
    return "No"

def get_difficulty(keyword):
    try:
        results = youtube.search().list(
            q=keyword,
            part='id',
            type='video',
            maxResults=50
        ).execute()
        total = len(results.get("items", []))
        score = max(1, min(100, 100 - total * 2))  # The fewer results, the easier
        return score
    except:
        return random.randint(30, 90)

@app.route('/', methods=['GET', 'POST'])
def index():
    keyword_data = []
    base_keyword = ''

    if request.method == 'POST':
        base_keyword = request.form['keyword']
        suggestions = get_youtube_keywords(base_keyword)

        for keyword in suggestions:
            volume = get_search_volume(keyword)
            difficulty = get_difficulty(keyword)
            trending = is_trending(keyword)
            keyword_data.append({
                'keyword': keyword,
                'volume': volume,
                'difficulty': difficulty,
                'trending': trending
            })

    return render_template('index.html', keywords=keyword_data, base=base_keyword)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=10000)
