from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)

YOUTUBE_API_KEY = "AIzaSyDB3uRLRelUIy_4K3Im2NOGKDWzTbb7bCc"
YOUTUBE_SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"

@app.route('/', methods=['GET', 'POST'])
def index():
    keywords = []
    base = ''
    if request.method == 'POST':
        base = request.form['keyword']
        params = {
            'part': 'snippet',
            'q': base,
            'type': 'video',
            'maxResults': 50,
            'key': YOUTUBE_API_KEY
        }
        response = requests.get(YOUTUBE_SEARCH_URL, params=params)
        if response.status_code == 200:
            data = response.json()
            keywords = [item['snippet']['title'] for item in data.get('items', [])]
        else:
            keywords = ["Erreur de récupération des données."]
    return render_template('index.html', keywords=keywords, base=base)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
