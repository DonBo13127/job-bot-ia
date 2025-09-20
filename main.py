import os
import time
import smtplib
from email.message import EmailMessage
from datetime import datetime
import schedule

from scraper import scrape_ai_with_email
from gpt_utils import generate_cover_letter_html
from sheets_utils import connect_sheets_by_id, save_job_to_sheet

# ===========================
# Variables d'environnement
# ===========================
SMTP_EMAIL = os.getenv("SMTP_EMAIL")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
CV_LINK_FR = os.getenv("CV_LINK_FR")
CV_LINK_ES = os.getenv("CV_LINK_ES")
GPT_API_KEY = os.getenv("OPENAI_API_KEY")

SHEET_JSON = "absolute-bonsai-459420-q4-dddac3ebbb21.json"
SHEET_ID = "1Rgd-OuFHA-nXaBPBaZyVlFv7cTsphHScPih4-jn9st8"

IMAGE_URL = "https://img.freepik.com/photos-gratuite/specialiste-informatique-dans-ferme-serveurs-minimisant-defaillances-machines_264385749.htm"

# ===========================
# Connexion Google Sheet
# ===========================
sheet = connect_sheets_by_id(SHEET_JSON, SHEET_ID)

# ===========================
# Fonction d'envoi email
# ===========================
def send_email(job, html_content, cv_link, language="fr"):
    recipient = job.get("apply_email")
    if not recipient:
        print(f"[Email] Pas d'adresse pour {job.get('title')}")
        return

    msg = EmailMessage()
    msg["Subject"] = f"Candidature : {job.get('title')}"
    msg["From"] = SMTP_EMAIL
    msg["To"] = recipient

    msg.set_content("Votre client email ne supporte pas le HTML.")
    msg.add_alternative(html_content, subtype="html")

    # Ajouter les CV en pièce jointe
    for cv_url in [CV_LINK_FR, CV_LINK_ES]:
        try:
            import requests
            resp = requests.get(cv_url)
            filename = cv_url.split("/")[-1]
            msg.add_attachment(resp.content, maintype="application", subtype="pdf", filename=filename)
        except Exception as e:
            print(f"[Attachment] Erreur ajout CV {cv_url}: {e}")

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(SMTP_EMAIL, SMTP_PASSWORD)
            server.send_message(msg)
        print(f"[Email] Envoyé : {job.get('title')} à {recipient}")
    except Exception as e:
        print(f"[Email] Erreur : {e}")

# ===========================
# Fonction principale
# ===========================
def job_bot():
    print(f"\n🚀 Démarrage du bot : {datetime.now()}")
    jobs = scrape_ai_with_email()
    print(f"✅ {len(jobs)} annonces IA avec email trouvées.")

    for job in jobs:
        title = job.get("title")
        print(f"\n💼 {title}")

        # Détection langue (fr/es)
        language = "es" if any(w in title.lower() for w in ["ingeniero", "automatización"]) else "fr"

        # Génération lettre HTML
        html_content = generate_cover_letter_html(job, language, IMAGE_URL)

        # Envoi email
        send_email(job, html_content, CV_LINK_FR if language=="fr" else CV_LINK_ES, language)

        # Sauvegarde Google Sheet
        save_job_to_sheet(sheet, job, language)

# ===========================
# Scheduler toutes les heures
# ===========================
schedule.every(1).hours.do(job_bot)
print("🕒 Scheduler activé : le bot s'exécutera toutes les heures.")

# Première exécution immédiate
job_bot()

while True:
    schedule.run_pending()
    time.sleep(60)
