import os
import schedule
import time
from scraper import scrape_all_ai_with_email
from gpt_utils import generate_cover_letter_html
from email_utils import send_email_gmail
from sheets_utils import connect_sheets, save_job

# Variables d'environnement
SHEET_JSON = os.getenv("SHEET_JSON")  # chemin vers le JSON du service account
SHEET_URL = os.getenv("SHEET_URL")    # URL complète du Google Sheet
SMTP_EMAIL = os.getenv("SMTP_EMAIL")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
CV_LINK_FR = os.getenv("CV_LINK_FR")
CV_LINK_ES = os.getenv("CV_LINK_ES")
IMAGE_URL = "https://image.freepik.com/photos-gratuite/specialiste-informatique-dans-ferme-serveurs-minimisant-defaillances-machines_264385749.htm"

# Connexion au Google Sheet
sheet = connect_sheets(SHEET_JSON, SHEET_URL)

def run_bot():
    print("🚀 Démarrage du bot de candidature automatique...")

    jobs = scrape_all_ai_with_email()
    if not jobs:
        print("📭 Aucune offre trouvée.")
        return

    print(f"✅ {len(jobs)} offres collectées.\n")

    for i, job in enumerate(jobs, 1):
        print(f"\n--- Offre {i}/{len(jobs)} ---")
        print(f"💼 {job.get('title')} chez {job.get('company')} ({job.get('source')})")

        lang = "es" if any(word in job.get("title", "").lower() for word in ["ingeniero", "pruebas", "automatización"]) else "fr"

        # Génération de la lettre HTML
        html_letter = generate_cover_letter_html(job, lang, IMAGE_URL, CV_LINK_FR, CV_LINK_ES)

        # Envoi email
        send_email_gmail(job.get("apply_email"), f"Candidature : {job.get('title')}", html_letter, CV_LINK_FR if lang=="fr" else CV_LINK_ES)

        # Sauvegarde dans Google Sheets
        save_job(sheet, job, lang)

    print("\n🎯 Processus terminé.")

# Exécution immédiate
run_bot()

# Planification toutes les heures
schedule.every(1).hours.do(run_bot)
print("🕒 Scheduler activé : exécution toutes les heures.")

while True:
    schedule.run_pending()
    time.sleep(30)
