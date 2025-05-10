from flask import Flask, render_template, request
from pytrends.request import TrendReq
from bs4 import BeautifulSoup
import requests
import os

app = Flask(__name__)

def get_trending_status(keyword):
    pytrends = TrendReq(hl='en-US', tz=360)
    pytrends.build_payload([keyword], cat=0, timeframe='now 7-d', geo='', gprop='')
    data = pytrends.interest_over_time()
    if not data.empty and keyword in data.columns:
        recent = data[keyword].values[-3:]
        trend = "Rising" if all(x <= y for x, y in zip(recent, recent[1:])) else "Stable" if recent[-1] == recent[0] else "Falling"
    else:
        trend = "Unknown"
    return trend

def get_youtube_keywords(query):
    url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')
    keywords = []
    for tag in soup.find_all('a'):
        title = tag.get('title')
        if title and query.lower() in title.lower():
            keywords.append(title)
    return list(set(keywords))[:50]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/keywords', methods=['POST'])
def keywords():
    query = request.form['query']
    keywords = get_youtube_keywords(query)
    keyword_data = []
    for keyword in keywords:
        trend = get_trending_status(keyword)
        difficulty = max(0, min(100, 100 - len(keyword) * 2))  # Simulated difficulty
        keyword_data.append({
            'keyword': keyword,
            'volume': 1000 + len(keyword) * 10,
            'difficulty': difficulty,
            'trend': trend
        })
    keyword_data.sort(key=lambda x: x['difficulty'])
    return render_template('index.html', keyword_data=keyword_data, query=query)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
