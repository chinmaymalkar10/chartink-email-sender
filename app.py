from flask import Flask, render_template, jsonify
from chartink_fetcher import start_background_task
import os

app = Flask(__name__)

# Start background fetcher
start_background_task()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/logs')
def get_logs():
    if not os.path.exists("log.txt"):
        return jsonify([])
    with open("log.txt", "r") as f:
        lines = f.readlines()
    return jsonify(lines[-20:])  # last 20 logs

if __name__ == '__main__':
    app.run(debug=True)
