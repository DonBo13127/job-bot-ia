import os
import smtplib
from email.message import EmailMessage
from email.utils import formataddr
from email.mime.base import MIMEBase
from email import encoders
import requests

SMTP_EMAIL = os.getenv("SMTP_EMAIL")  # ex: tonmail@gmail.com
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")  # mot de passe application Gmail

def send_email_gmail(to_email, subject, html_content, cv_url, image_url):
    msg = EmailMessage()
    msg["From"] = formataddr(("Yacine Bedhouche", SMTP_EMAIL))
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.set_content("Veuillez afficher cet email en HTML pour voir le contenu complet.")

    # HTML
    msg.add_alternative(html_content, subtype="html")

    # Pièces jointes : CV
    try:
        cv_data = requests.get(cv_url).content
        cv_name = cv_url.split("/")[-1].split("?")[0]
        msg.add_attachment(cv_data, maintype="application", subtype="pdf", filename=cv_name)
    except Exception as e:
        print(f"[Email] Erreur CV : {e}")

    # Image en pièce jointe
    try:
        img_data = requests.get(image_url).content
        img_name = image_url.split("/")[-1].split("?")[0]
        msg.add_attachment(img_data, maintype="image", subtype="jpeg", filename=img_name)
    except Exception as e:
        print(f"[Email] Erreur image : {e}")

    # Envoi via SMTP Gmail
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(SMTP_EMAIL, SMTP_PASSWORD)
            server.send_message(msg)
        print(f"📩 Email envoyé à {to_email}")
    except Exception as e:
        print(f"[Email] Erreur : {e}")
