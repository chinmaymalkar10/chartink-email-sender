import threading
import time
import requests
from bs4 import BeautifulSoup
from email_sender import send_email

charting_link = "https://chartink.com/screener/"
charting_url = "https://chartink.com/screener/process"

condition = "( {57960} ( [0] 15 minute close > [-1] 15 minute max ( 20 , [0] 15 minute close ) and [0] 15 minute volume > [0] 15 minute sma ( volume,20 ) ) ) "

def getData(payload):
    payload = {'scan_clause': payload}
    try:
        with requests.Session() as s:
            r = s.get(charting_link)
            soup = BeautifulSoup(r.text, "html.parser")
            csrf = soup.select_one("[name='csrf-token']")['content']
            s.headers['x-csrf-token'] = csrf
            r = s.post(charting_url, data=payload)

            df = []
            for item in r.json()['data']:
                df.append(item['name'])
            return df
    except Exception as e:
        print(f"Chartink fetch error: {e}")
        return []

def poll_chartink():
    while True:
        data = getData(condition)
        if data:
            for stock in data:
                send_email(stock)
        time.sleep(60)  # poll every 1 minute

def start_background_task():
    t = threading.Thread(target=poll_chartink, daemon=True)
    t.start()
