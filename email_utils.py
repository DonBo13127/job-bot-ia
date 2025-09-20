import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import requests

SMTP_EMAIL = os.getenv("SMTP_EMAIL")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

CV_LINK_FR = os.getenv("CV_LINK_FR")
CV_LINK_ES = os.getenv("CV_LINK_ES")

def send_email_with_attachments(to_email, html_content, language="fr"):
    if not to_email:
        print("[Email] Aucun email trouvé, skip.")
        return

    cv_link = CV_LINK_FR if language == "fr" else CV_LINK_ES

    msg = MIMEMultipart()
    msg['From'] = SMTP_EMAIL
    msg['To'] = to_email
    msg['Subject'] = "Candidature"

    msg.attach(MIMEText(html_content, 'html'))

    # Ajouter CV en pièce jointe
    try:
        r = requests.get(cv_link)
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(r.content)
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename="CV.pdf"')
        msg.attach(part)
    except Exception as e:
        print(f"[Email] Erreur ajout CV : {e}")

    # Envoi
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(SMTP_EMAIL, SMTP_PASSWORD)
            server.send_message(msg)
        print(f"[Email] Envoyé à {to_email}")
    except Exception as e:
        print(f"[Email] Erreur envoi : {e}")
