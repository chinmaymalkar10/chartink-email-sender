import threading
import time
import requests
from bs4 import BeautifulSoup
from email_sender import send_email

charting_link = "https://chartink.com/screener/"
charting_url = "https://chartink.com/screener/process"
stocks = [
    "ACC", "AFFLE", "ASTRAL", "AUROPHARMA", "BAJAJFINSV", "BANKBARODA", "BDL", "BHARTIARTL", "CDSL",
    "CHOLAFIN", "CIPLA", "DRREDDY", "GLENMARK", "MEDANTA", "HCLTECH", "HDFCBANK", "HAL", "HINDUNILVR",
    "ICICIGI", "INDUSINDBK", "INFY", "LT", "LUPIN", "LODHA", "MAXHEALTH", "NESTLEIND", "PATANJALI",
    "POLICYBZR", "PIDILITIND", "PVRINOX", "RADICO", "RELIANCE", "SBICARD", "SRF", "SBIN", "SUNPHARMA",
    "TATACHEM", "TCS", "TATACONSUM", "TECHM", "TITAN", "TORNTPHARM", "TORNTPOWER", "UBL", "UNITDSPR", "VOLTAS"
]

condition = "( ( [0] 5 minute adx ( 14 ) > 25 and [0] 5 minute close >= 800 and [0] 5 minute close <= 4000 and [0] 5 minute close < [0] 5 minute sma ( close,8 ) and [0] 5 minute close < 1 day ago low and [-1] 5 minute close > 1 day ago low and abs ( 1 day ago low - latest open ) <= latest open * 0.007 ) ) "

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
        time.sleep(240)  # poll every 1 minute

def start_background_task():
    t = threading.Thread(target=poll_chartink, daemon=True)
    t.start()
