from flask import Flask, request, render_template
from difflib import SequenceMatcher

app = Flask(__name__)

def get_keywords(base_keyword):
    related = [f"{base_keyword} tutorial", f"{base_keyword} 2025", f"how to {base_keyword}", f"{base_keyword} for beginners"]
    data = []
    for keyword in related:
        difficulty = int(100 - SequenceMatcher(None, keyword, base_keyword).ratio() * 100)
        data.append({
            "keyword": keyword,
            "search_volume": f"{1000 + difficulty * 20}",
            "difficulty": difficulty,
            "trend": "Rising" if difficulty < 50 else "Stable"
        })
    return sorted(data, key=lambda x: x["difficulty"])

@app.route('/', methods=['GET', 'POST'])
def index():
    keyword_data = []
    base_keyword = ""
    if request.method == 'POST':
        base_keyword = request.form['keyword']
        keyword_data = get_keywords(base_keyword)
    return render_template('index.html', keywords=keyword_data, base=base_keyword)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
