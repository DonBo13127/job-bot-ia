import os
import schedule
import time
from scraper import scrape_all_ai_with_email
from gpt_utils import generate_cover_letter_html
from email_utils import send_email_gmail
from sheets_utils import connect_sheets, save_job

# Variables d'environnement
GMAIL_EMAIL = os.getenv("GMAIL_EMAIL")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")
CV_LINK_FR = os.getenv("CV_LINK_FR")
CV_LINK_ES = os.getenv("CV_LINK_ES")
IMAGE_URL = "https://img.freepik.com/photos-gratuite/specialiste-informatique-dans-ferme-serveurs-minimisant-defaillances-machines_264385749.htm"

# Google Sheet
SHEET_JSON = "absolute-bonsai-459420-q4-dddac3ebbb21.json"
SHEET_URL = "https://docs.google.com/spreadsheets/d/1Rgd-OuFHA-nXaBPBaZyVlFv7cTsphHScPih4-jn9st8/edit#gid=0"
sheet = connect_sheets(SHEET_JSON, SHEET_URL)

def run_bot():
    print("🚀 Démarrage du bot de candidature automatique...")

    jobs = scrape_all_ai_with_email()
    if not jobs:
        print("📭 Aucune offre IA avec email trouvée.")
        return

    print(f"✅ {len(jobs)} offres IA collectées.\n")

    for i, job in enumerate(jobs, 1):
        print(f"\n--- Offre {i}/{len(jobs)} ---")
        print(f"💼 {job.get('title')} chez {job.get('company')} ({job.get('source')})")
        lang = job.get("lang", "fr")
        email = job.get("apply_email")
        if not email:
            print("[Email] Ignorée car aucun email fourni.")
            continue

        # Génération lettre HTML
        letter_html = generate_cover_letter_html(job, lang, IMAGE_URL, CV_LINK_FR, CV_LINK_ES)

        # Envoi email
        send_email_gmail(email, f"Candidature : {job.get('title')}", letter_html,
                         GMAIL_EMAIL, GMAIL_APP_PASSWORD, CV_LINK_FR if lang=="fr" else CV_LINK_ES)

        # Sauvegarde Google Sheets
        save_job(sheet, job)

    print("\n🎯 Processus terminé.")

# Exécution immédiate
run_bot()

# Planification toutes les heures
schedule.every(1).hours.do(run_bot)
print("🕒 Scheduler activé : exécution toutes les heures.")

while True:
    schedule.run_pending()
    time.sleep(60)
