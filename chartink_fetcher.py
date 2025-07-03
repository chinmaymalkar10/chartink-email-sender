import threading
import time
import requests
from bs4 import BeautifulSoup
from email_sender import send_notification
from datetime import datetime, timedelta
import pytz

last_alerts = {}
IST = pytz.timezone("Asia/Kolkata")
charting_link = "https://chartink.com/screener/"
charting_url = "https://chartink.com/screener/process"
stocks = [
    "ACC", "AFFLE", "ASTRAL", "AUROPHARMA", "BAJAJFINSV", "BANKBARODA", "BDL", "BHARTIARTL", "CDSL",
    "CHOLAFIN", "CIPLA", "DRREDDY", "GLENMARK", "MEDANTA", "HCLTECH", "HDFCBANK", "HAL", "HINDUNILVR",
    "ICICIGI", "INDUSINDBK", "INFY", "LT", "LUPIN", "LODHA", "MAXHEALTH", "NESTLEIND", "PATANJALI",
    "POLICYBZR", "PIDILITIND", "PVRINOX", "RADICO", "RELIANCE", "SBICARD", "SRF", "SBIN", "SUNPHARMA",
    "TATACHEM", "TCS", "TATACONSUM", "TECHM", "TITAN", "TORNTPHARM", "TORNTPOWER", "UBL", "UNITDSPR", "VOLTAS"
]

condition_sell = "( ( [0] 5 minute adx ( 14 ) > 25 and [0] 5 minute close >= 800 and [0] 5 minute close <= 4000 and [0] 5 minute close < [0] 5 minute sma ( close,8 ) and [0] 5 minute close < 1 day ago low and [-1] 5 minute close > 1 day ago low and abs ( 1 day ago low - latest open ) <= latest open * 0.007 ) ) "

condition_buy = "( ( [0] 5 minute adx ( 14 ) > 25 and [0] 5 minute close >= 800 and [0] 5 minute close <= 4000 and [0] 5 minute close > [0] 5 minute sma ( close,8 ) and [0] 5 minute close > 1 day ago high and [0] 5 minute close > 1 day ago high and [-1] 5 minute close <= 1 day ago high and abs ( 1 day ago high - latest open ) <= latest open * 0.007 ) ) "


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
                if item['nsecode'] in stocks:
                    df.append(item['nsecode'])
            return df
    except Exception as e:
        print(f"Chartink fetch error: {e}")
        return []

def poll_chartink():
    global last_alerts

    while True:
        now = datetime.now(IST)
        
        # ---- Buy Entry Check ----
        stocks = ""
        buy_stocks = getData(condition_buy)
        for stock in buy_stocks:
            key = (stock, "Buy Entry")
            last_time = last_alerts.get(key)

            if not last_time or now - last_time > timedelta(minutes=10):
                stocks += stock + " , "
                last_alerts[key] = now  # Update alert time

        if stocks:
            send_notification(stocks.strip(" ,"), "Buy Entry")

        # ---- Sell Entry Check ----
        stocks = ""
        sell_stocks = getData(condition_sell)
        for stock in sell_stocks:
            key = (stock, "Sell Entry")
            last_time = last_alerts.get(key)

            if not last_time or now - last_time > timedelta(minutes=10):
                stocks += stock + " , "
                last_alerts[key] = now  # Update alert time

        if stocks:
            send_notification(stocks.strip(" ,"), "Sell Entry")

        time.sleep(30)

def start_background_task():
    t = threading.Thread(target=poll_chartink, daemon=True)
    t.start()
