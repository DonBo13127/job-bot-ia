import time
import schedule
from scraper import scrape_all_with_email
from gpt_utils import generate_cover_letter_html
from sheets_utils import connect_sheets, save_job
from email_utils import send_email_gmail
from langdetect import detect

SHEET_JSON = "absolute-bonsai-459420-q4-dddac3ebbb21.json"
SHEET_URL = "https://docs.google.com/spreadsheets/d/1Rgd-OuFHA-nXaBPBaZyVlFv7cTsphHScPih4-jn9st8/edit"
IMAGE_URL = "https://cdn.pixabay.com/photo/2017/08/10/07/28/computer-2616432_1280.jpg"  # Exemple image
CV_PATH = "CV.pdf"

def process_jobs():
    print("🚀 Démarrage du bot de candidature automatique...")
    sheet = connect_sheets(SHEET_JSON, SHEET_URL)
    jobs = scrape_all_with_email()
    print(f"✅ {len(jobs)} offres IA collectées.\n")

    for idx, job in enumerate(jobs, 1):
        print(f"--- Offre {idx}/{len(jobs)} ---")
        lang = detect(job['title'])
        if lang not in ['fr', 'es']:
            lang = 'fr'
        html_letter = generate_cover_letter_html(job['title'], job.get('company', ''), lang, IMAGE_URL)

        try:
            send_email_gmail(job['email'], f"Candidature: {job['title']}", html_letter, attachments=[CV_PATH])
            print(f"[Email] Envoyé à {job['email']}")
        except Exception as e:
            print(f"[Email] Erreur : {e}")

        save_job(sheet, job)
        print(f"🗂 Offre enregistrée : {job['title']}\n")

    print("🎯 Processus terminé.")

# Exécution immédiate
process_jobs()

# Scheduler toutes les heures
schedule.every(1).hours.do(process_jobs)
print("🕒 Scheduler activé : exécution toutes les heures.")

while True:
    schedule.run_pending()
    time.sleep(60)
