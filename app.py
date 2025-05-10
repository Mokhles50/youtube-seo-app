from flask import Flask, render_template, request
from random import randint

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    results = []
    if request.method == 'POST':
        query = request.form.get('query')
        if query:
            # Simulate 10 keyword suggestions with dummy data
            for i in range(10):
                results.append({
                    'keyword': f"{query} suggestion {i+1}",
                    'volume': f"{randint(1000, 10000)}",
                    'difficulty': randint(10, 90),
                    'trend': 'Up' if i % 2 == 0 else 'Stable'
                })
    return render_template('index.html', results=results)
