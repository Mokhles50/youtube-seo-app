from flask import Flask, render_template, request
import requests
import random

app = Flask(__name__)

YOUTUBE_API_KEY = 'AIzaSyDB3uRLRelUIy_4K3Im2NOGKDWzTbb7bCc'

def fetch_related_keywords(query):
    url = f'https://suggestqueries.google.com/complete/search?client=firefox&ds=yt&q={query}'
    response = requests.get(url)
    if response.status_code == 200:
        suggestions = response.json()[1]
        keywords = []
        for keyword in suggestions[:50]:
            keywords.append({
                'keyword': keyword,
                'volume': random.randint(1000, 100000),
                'difficulty': round(random.uniform(0.1, 1.0), 2),
                'trending': random.choice(['Yes', 'No'])
            })
        return keywords
    return []

@app.route('/', methods=['GET', 'POST'])
def index():
    keywords = []
    base_keyword = ''
    if request.method == 'POST':
        base_keyword = request.form['keyword']
        keywords = fetch_related_keywords(base_keyword)
    return render_template('index.html', keywords=keywords, base=base_keyword)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=10000)
