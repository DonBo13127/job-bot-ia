import os
import time
import schedule
from scraper import scrape_all_with_email  # Scraper uniquement les offres avec email
from gpt_utils import generate_cover_letter_html
from email_utils import send_email_with_attachments
from sheets_utils import connect_sheets, save_job

# ===========================
# Variables d'environnement
# ===========================
SHEET_JSON = os.getenv("SHEET_JSON")  # Chemin vers ton JSON
SHEET_NAME = "Replit"  # Nom exact de ton Google Sheet

# Connexion Google Sheets
sheet = connect_sheets(SHEET_JSON, SHEET_NAME)

# ===========================
# Fonction principale
# ===========================
def job_runner():
    print("\n🚀 Démarrage du bot de candidature automatique...\n")
    jobs = scrape_all_with_email()
    if not jobs:
        print("📭 Aucune offre trouvée.")
        return

    print(f"✅ {len(jobs)} offres collectées.\n")

    for i, job in enumerate(jobs, 1):
        print(f"\n--- Offre {i}/{len(jobs)} ---")
        print(f"💼 {job.get('title')} chez {job.get('company')} ({job.get('source')})")
        print(f"📧 Email contact : {job.get('apply_email')}")

        # Détection de langue
        lang = "es" if any(w in job.get("title", "").lower() for w in ["ingeniero", "qa", "pruebas", "automatización"]) else "fr"

        # Génération lettre + image
        letter_html = generate_cover_letter_html(job, lang)

        # Envoi email avec CV et image
        send_email_with_attachments(job.get("apply_email"), letter_html, lang)

        # Sauvegarde dans Google Sheets
        save_job(sheet, job, lang)

    print("\n🎯 Processus terminé.")

# ===========================
# Exécution immédiate
# ===========================
job_runner()

# ===========================
# Scheduler toutes les heures
# ===========================
schedule.every().hour.do(job_runner)
print("🕒 Scheduler activé : exécution toutes les heures.")

while True:
    schedule.run_pending()
    time.sleep(60)
