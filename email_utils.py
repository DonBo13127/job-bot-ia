import smtplib
from email.message import EmailMessage
from email.utils import make_msgid
import requests

def send_email_gmail(to_email, subject, html_content, gmail_email, gmail_app_password, cv_file_link):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = gmail_email
    msg["To"] = to_email

    msg.add_alternative(html_content, subtype="html")

    # Ajouter le CV en pièce jointe
    try:
        r = requests.get(cv_file_link)
        if r.status_code == 200:
            msg.add_attachment(r.content, maintype="application", subtype="pdf", filename="CV.pdf")
    except Exception as e:
        print(f"[Email] Erreur en attachant le CV : {e}")

    # Envoi via Gmail
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(gmail_email, gmail_app_password)
            server.send_message(msg)
        print(f"📩 Email envoyé à {to_email}")
    except Exception as e:
        print(f"[Email] Erreur : {e}")
