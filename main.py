import os
import time
import schedule
from scraper import scrape_all
from mail_utils import generate_html_letter, send_email
from sheets_utils import connect_sheets, save_job
import openai

# Variables d'environnement
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SMTP_EMAIL = os.getenv("SMTP_EMAIL")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
CV_LINK_FR = os.getenv("CV_LINK_FR")
CV_LINK_ES = os.getenv("CV_LINK_ES")
SHEET_JSON = "absolute-bonsai-459420-q4-dddac3ebbb21.json"
SHEET_NAME = "JobBot"

openai.api_key = OPENAI_API_KEY
sheet = connect_sheets(SHEET_JSON, SHEET_NAME)

def detect_language(text):
    keywords_es = ["ingeniero", "automatización", "pruebas", "tecnología"]
    if any(k in text.lower() for k in keywords_es):
        return "es"
    return "fr"

def generate_cover_letter(job, language):
    prompt_fr = f"Rédige une lettre courte et percutante pour postuler au poste '{job['title']}' chez '{job['company']}'."
    prompt_es = f"Escribe una carta breve y convincente para el puesto '{job['title']}' en '{job['company']}'."
    prompt = prompt_fr if language == "fr" else prompt_es

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"[GPT] Erreur: {e}")
        return ""

def job_cycle():
    print("🚀 Démarrage du bot...")
    jobs = scrape_all()
    print(f"✅ {len(jobs)} offres collectées.")

    for job in jobs:
        lang = detect_language(job["title"])
        letter = generate_cover_letter(job, lang)
        html_content = generate_html_letter(letter, "https://image.freepik.com/photos-gratuite/specialiste-informatique-dans-ferme-serveurs-minimisant-defaillances-machines_264385749.jpg")
        cv_file = CV_LINK_FR if lang == "fr" else CV_LINK_ES
        save_job(sheet, job, lang)
        send_email(SMTP_EMAIL, SMTP_PASSWORD, job.get("apply_email"), f"Candidature: {job['title']}", html_content, attachments=[cv_file])
    print("🎯 Cycle terminé.\n")

# Scheduler toutes les heures
schedule.every().hour.do(job_cycle)
print("🕒 Scheduler activé : le bot s'exécutera toutes les heures.")

while True:
    schedule.run_pending()
    time.sleep(60)
