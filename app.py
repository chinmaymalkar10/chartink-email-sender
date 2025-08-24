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
    buy_logs, sell_logs, adx_buy_logs = [], [], []
    if os.path.exists("log.txt"):
        with open("log.txt", "r") as f:
            lines = f.readlines()
        for line in lines[-100:]:  # Only last 100 entries
            if "ADX Buy Entry" in line:
                adx_buy_logs.append(line.strip())
            elif "Buy Entry" in line:   # put this after ADX to avoid overlap
                buy_logs.append(line.strip())
            elif "Sell Entry" in line:
                sell_logs.append(line.strip())
    return jsonify({
        "buy": buy_logs,
        "sell": sell_logs,
        "adx_buy": adx_buy_logs
    })

if __name__ == '__main__':
    app.run(debug=True)
