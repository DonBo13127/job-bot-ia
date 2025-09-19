# email_sender.py
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os

def send_email(to_email, subject, body):
    msg = MIMEMultipart()
    msg['From'] = os.getenv("SMTP_EMAIL")
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp-mail.outlook.com', 587)
        server.starttls()
        server.login(os.getenv("SMTP_EMAIL"), os.getenv("SMTP_PASSWORD"))
        text = msg.as_string()
        server.sendmail(os.getenv("SMTP_EMAIL"), to_email, text)
        server.quit()
        print(f"[Email] Envoyé à {to_email}")
        return True
    except Exception as e:
        print(f"[Email] Échec envoi: {e}")
        return False
