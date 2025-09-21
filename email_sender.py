# import smtplib
# from email.message import EmailMessage
from datetime import datetime
import pytz
from twilio.rest import Client
import os
from dotenv import load_dotenv

# Load credentials from .env
load_dotenv()

# EMAIL_SENDER = os.getenv('EMAIL_SENDER')
# EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
# EMAIL_RECEIVER = os.getenv('EMAIL_RECEIVER')
account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
client = Client(account_sid, auth_token)
TWILIO_WHATSAPP_FROM = os.getenv('TWILIO_WHATSAPP_FROM')
WHATSAPP_TO = os.getenv('WHATSAPP_TO')

def send_notification(stock_name, signal_type):
    # send_email(stock_name, signal_type)
    send_whatsapp(stock_name, signal_type)

# def send_email(stock_name, signal_type):
#     msg = EmailMessage()
#     msg['Subject'] = f"{signal_type} Alert"
#     msg['From'] = EMAIL_SENDER
#     msg['To'] = EMAIL_RECEIVER
#     body = f"{signal_type} detected for stock: {stock_name}"
#     msg.set_content(body)

#     try:
#         with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
#             smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)
#             smtp.send_message(msg)
#         log(f"{signal_type} | {stock_name}")
#     except Exception as e:
#         log(f"Error sending email: {e}")
        
def send_whatsapp(stock_name, signal_type):
    try:
        body = f"{signal_type} detected for stock: {stock_name}"
        message = client.messages.create(
                  from_=f'whatsapp:{TWILIO_WHATSAPP_FROM}',
                  body=body,
                  to=f'whatsapp:{WHATSAPP_TO}')
        log(f"{signal_type} | {stock_name}")
    except Exception as e:
        log(f"WhatsApp error for {signal_type} - {stock_name}: {e}")

def log(message):
    ist = pytz.timezone("Asia/Kolkata")
    ist_time = datetime.now(ist).strftime('%Y-%m-%d %H:%M:%S')
    with open("log.txt", "a") as f:
        f.write(f"[{ist_time}] {message}\n")
