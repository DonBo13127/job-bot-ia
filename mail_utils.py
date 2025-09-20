import smtplib
from email.message import EmailMessage
import mimetypes
import requests
from io import BytesIO

def generate_html_letter(letter_text, image_url):
    return f"""
    <html>
      <body style="font-family:Arial,sans-serif;line-height:1.5;color:#333;">
        <h2 style="color:#2E86C1;">Candidature spontanée</h2>
        <p>{letter_text}</p>
        <img src="{image_url}" alt="Illustration IA" style="width:600px;margin-top:20px;">
      </body>
    </html>
    """

def send_email(smtp_email, smtp_pass, recipient, subject, html_content, attachments=[]):
    if not recipient:
        print("[Email] Aucun destinataire, email non envoyé.")
        return

    msg = EmailMessage()
    msg["From"] = smtp_email
    msg["To"] = recipient
    msg["Subject"] = subject
    msg.set_content("Merci de consulter ce mail en HTML.")
    msg.add_alternative(html_content, subtype="html")

    # Ajout des pièces jointes
    for file_path in attachments:
        with open(file_path, "rb") as f:
            data = f.read()
            maintype, subtype = mimetypes.guess_type(file_path)[0].split("/")
            msg.add_attachment(data, maintype=maintype, subtype=subtype, filename=file_path.split("/")[-1])

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(smtp_email, smtp_pass)
            server.send_message(msg)
        print(f"📩 Email envoyé à {recipient}")
    except Exception as e:
        print(f"[Email] Erreur: {e}")
