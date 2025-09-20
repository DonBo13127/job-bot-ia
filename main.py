import os
import schedule
import time
from datetime import datetime
from scraper import scrape_all_with_email
from gpt_utils import generate_cover_letter_html
from email_utils import send_email_gmail
from sheets_utils import connect_sheets, save_job

# Configuration Google Sheets
SHEET_JSON = "absolute-bonsai-459420-q4-dddac3ebbb21.json"
SHEET_NAME = "Replit"

sheet = connect_sheets(SHEET_JSON, SHEET_NAME)

# Variables
CV_LINK_FR = "https://www.dropbox.com/...fr.pdf?dl=0"
CV_LINK_ES = "https://www.dropbox.com/...es.docx?dl=0"
IMAGE_URL = "https://img.freepik.com/photos-gratuite/specialiste-informatique-dans-ferme-serveurs-minimisant-defaillances-machines_264385749.htm"

def run_bot():
    print(f"\n🚀 Démarrage du bot : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    jobs = scrape_all_with_email()
    print(f"✅ {len(jobs)} offres collectées.")
    
    for job in jobs:
        email = job.get("apply_email")
        if not email:
            continue
        
        title_lower = job.get("title", "").lower()
        lang = "es" if any(w in title_lower for w in ["ingeniero", "qa", "automatización"]) else "fr"
        
        letter_html = generate_cover_letter_html(job, lang, IMAGE_URL, CV_LINK_FR, CV_LINK_ES)
        
        send_email_gmail(email, f"Candidature : {job.get('title')}", letter_html,
                         CV_LINK_FR if lang=="fr" else CV_LINK_ES, IMAGE_URL)
        
        save_job(sheet, job, lang)
    
    print("🎯 Processus terminé.\n")

# Exécution immédiate
run_bot()

# Scheduler toutes les heures
schedule.every(1).hours.do(run_bot)
print("🕒 Scheduler activé : exécution toutes les heures.")

while True:
    schedule.run_pending()
    time.sleep(10)
