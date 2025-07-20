## filepath: /c:/Users/priya/Documents/reddit-sentiment-polarity/app.py
from flask import Flask, render_template, request, redirect, url_for
from main import searchCommentsAndAnalyze  # Import your existing function
from auth import authenticate  # Import the authenticate function

app = Flask(__name__)

# Initialize the Reddit instance using the authenticate function
reddit = authenticate()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/results', methods=['POST'])
def results():
    topic = request.form['topic']
    key_words = request.form['key_words']
    sentiments, texts = searchCommentsAndAnalyze(reddit, topic)
    return render_template('results.html', sentiments=sentiments, texts=texts, zip=zip)

if __name__ == '__main__':
    app.run(debug=True)