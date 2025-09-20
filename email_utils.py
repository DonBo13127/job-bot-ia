import smtplib
from email.message import EmailMessage
import os
import mimetypes

SMTP_EMAIL = os.getenv("SMTP_EMAIL")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

def send_email_gmail(to_email, subject, html_content, attachment_url):
    if not to_email:
        print("[Email] Aucun email trouvé pour cette offre, skipped.")
        return

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = SMTP_EMAIL
    msg["To"] = to_email
    msg.set_content("Votre client email ne supporte pas le HTML")
    msg.add_alternative(html_content, subtype="html")

    # Télécharger et attacher le fichier CV
    try:
        import requests
        r = requests.get(attachment_url)
        filename = attachment_url.split("/")[-1]
        mime_type, _ = mimetypes.guess_type(filename)
        maintype, subtype = mime_type.split("/", 1)
        msg.add_attachment(r.content, maintype=maintype, subtype=subtype, filename=filename)
    except Exception as e:
        print(f"[Email] Erreur téléchargement CV : {e}")

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(SMTP_EMAIL, SMTP_PASSWORD)
            server.send_message(msg)
        print(f"📩 Email envoyé à {to_email}")
    except Exception as e:
        print(f"[Email] Erreur : {e}")
