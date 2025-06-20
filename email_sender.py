import smtplib
from email.message import EmailMessage
from datetime import datetime

EMAIL_SENDER = 'onliogs69@gmail.com'
EMAIL_PASSWORD = 'jfvp avby mhwj trlx'  # Use Gmail App Password
EMAIL_RECEIVER = 'chinmaymalkar10@gmail.com'

def send_email(stock_name):
    msg = EmailMessage()
    msg['Subject'] = "Sell Entry"
    msg['From'] = EMAIL_SENDER
    msg['To'] = EMAIL_RECEIVER
    msg.set_content(f"Sell signal for: {stock_name}")

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)
            smtp.send_message(msg)
        log(f"Email sent for: {stock_name}")
    except Exception as e:
        log(f"Error sending email: {e}")

def log(message):
    with open("log.txt", "a") as f:
        f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}\n")
