import os
import time
from scraper import scrape_all_with_email  # Scraper IA uniquement
from sheets_utils import connect_sheets, save_job
from gpt_utils import generate_cover_letter_html
from email_utils import send_email_gmail  # utilise Gmail avec mot de passe d'application

# ===========================
# Variables d'environnement
# ===========================
GMAIL_EMAIL = os.getenv("GMAIL_EMAIL")  # ton email Gmail
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")  # mot de passe d'application Gmail
SHEET_JSON = os.getenv("SHEET_JSON")  # ton fichier JSON du service account
SHEET_URL = "https://docs.google.com/spreadsheets/d/1Rgd-OuFHA-nXaBPBaZyVlFv7cTsphHScPih4-jn9st8/edit"  # ton sheet

# Connexion à Google Sheets
sheet = connect_sheets(SHEET_JSON, SHEET_URL)

def main():
    print("🚀 Démarrage du bot de candidature automatique...")

    jobs = scrape_all_with_email()
    if not jobs:
        print("📭 Aucune offre trouvée.")
        return

    print(f"✅ {len(jobs)} offres IA collectées.\n")

    for i, job in enumerate(jobs, 1):
        print(f"--- Offre {i}/{len(jobs)} ---")
        print(f"💼 {job.get('title')} chez {job.get('company')} ({job.get('source')})")

        # Génération de la lettre HTML
        lang = job.get("lang", "fr")
        letter_html = generate_cover_letter_html(job, lang)

        # Envoi de l'email via Gmail
        send_email_gmail(
            to_email=job.get("email"),
            subject=f"Candidature : {job.get('title')}",
            html_content=letter_html,
            attachments=[job.get("cv_fr"), job.get("cv_es")],  # chemins vers tes CV locaux
            from_email=GMAIL_EMAIL,
            app_password=GMAIL_APP_PASSWORD
        )

        # Sauvegarde dans Google Sheets
        save_job(sheet, job)

        print(f"🗂 Offre enregistrée : {job.get('title')}\n")

    print("🎯 Processus terminé.")

if __name__ == "__main__":
    main()
    print("🕒 Scheduler activé : exécution toutes les heures.")
    while True:
        time.sleep(3600)
        main()
