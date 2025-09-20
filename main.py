import os
import smtplib
from email.message import EmailMessage
import schedule
import time
from scraper import scrape_ai_with_email
from gpt_utils import generate_cover_letter_html
from sheets_utils import connect_sheets, save_job

SHEET_JSON = "absolute-bonsai-459420-q4-dddac3ebbb21.json"
SHEET_URL = "https://docs.google.com/spreadsheets/d/1Rgd-OuFHA-nXaBPBaZyVlFv7cTsphHScPih4-jn9st8/edit"
SMTP_EMAIL = os.getenv("SMTP_EMAIL")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

def detect_language(title):
    title = title.lower()
    if any(w in title for w in ["ingeniero", "automatización", "pruebas", "tecnología"]):
        return "es"
    return "fr"

def send_email(job, html_content):
    if not job.get("apply_email"):
        return False
    msg = EmailMessage()
    msg["Subject"] = f"Candidature : {job['title']}"
    msg["From"] = SMTP_EMAIL
    msg["To"] = job["apply_email"]
    msg.set_content("Votre client email ne supporte pas HTML")
    msg.add_alternative(html_content, subtype="html")

    # Ajouter CV en pièce jointe
    import requests
    from io import BytesIO
    for cv_url in [os.getenv("CV_LINK_FR"), os.getenv("CV_LINK_ES")]:
        resp = requests.get(cv_url)
        if resp.status_code==200:
            msg.add_attachment(resp.content, maintype="application", subtype="pdf", filename="CV.pdf")
            break

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(SMTP_EMAIL, SMTP_PASSWORD)
            server.send_message(msg)
        print(f"📩 Email envoyé à {job['apply_email']}")
        return True
    except Exception as e:
        print(f"[Email] Erreur : {e}")
        return False

def job_runner():
    print("🚀 Démarrage du bot IA...")
    sheet = connect_sheets(SHEET_JSON, SHEET_URL)
    jobs = scrape_ai_with_email()

    for job_item in jobs:
        lang = detect_language(job_item["title"])
        html_letter = generate_cover_letter_html(job_item, lang)
        if save_job(sheet, job_item, lang):
            send_email(job_item, html_letter)

# Exécution toutes les heures
schedule.every().hour.do(job_runner)
print("🕒 Scheduler activé : exécution toutes les heures.")

while True:
    schedule.run_pending()
    time.sleep(60)
