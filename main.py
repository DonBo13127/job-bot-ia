import os
import smtplib
from email.message import EmailMessage
from langdetect import detect
import openai
import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SMTP_EMAIL = os.getenv("SMTP_EMAIL")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
CV_LINK_FR = os.getenv("CV_LINK_FR")
CV_LINK_ES = os.getenv("CV_LINK_ES")
CREDENTIALS_FILE = "absolute-bonsai-459420-q4-dddac3ebbb21.json"
SHEET_NAME = "JobApplications"

openai.api_key = OPENAI_API_KEY

# Google Sheets setup
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, scope)
client = gspread.authorize(creds)
sheet = client.open(SHEET_NAME).sheet1

# Détection langue
def detect_language(text):
    try:
        lang = detect(text)
        return "fr" if lang == "fr" else "es"
    except:
        return "fr"

# Génération lettre + image
def generate_cover_letter(job, language="fr"):
    prompt = f"""
    Tu es un spécialiste en IA et RH. Rédige une lettre de motivation courte et percutante pour ce poste :
    {job['title']} chez {job['company']}
    URL : {job['url']}
    """
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=400
    )
    letter = response.choices[0].message.content.strip()
    # Ajouter image HTML
    letter_html = f'{letter}<br><img src="https://img.freepik.com/photos-gratuite/specialiste-informatique-dans-ferme-serveurs-minimisant-defaillances-machines_264385749.htm" width="400">'
    return letter, letter_html

# Envoi email
def send_email(job, letter_html, language="fr"):
    msg = EmailMessage()
    msg["Subject"] = f"Candidature : {job['title']}"
    msg["From"] = SMTP_EMAIL
    msg["To"] = job.get("apply_email", SMTP_EMAIL)
    msg.set_content(letter_html, subtype='html')
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(SMTP_EMAIL, SMTP_PASSWORD)
            server.send_message(msg)
        print(f"Email envoyé pour {job['title']}")
    except Exception as e:
        print(f"Erreur email : {e}")

# Vérifie si l'offre existe déjà dans Sheets
def exists_in_sheet(job):
    try:
        records = sheet.get_all_records()
        return any(r['URL'] == job['url'] for r in records)
    except:
        return False

# Sauvegarde dans Google Sheets
def save_to_sheets(job, language):
    if not exists_in_sheet(job):
        sheet.append_row([job['title'], job['company'], job['url'], language.upper()])
        print(f"Offre sauvegardée : {job['title']}")
    else:
        print(f"Offre déjà existante : {job['title']}")

# Exemple de job
jobs = [
    {"title":"QA Engineer", "company":"EntrepriseX", "url":"https://example.com/job1", "apply_email":"test@gmail.com"}
]

for job in jobs:
    lang = detect_language(job['title'])
    letter, letter_html = generate_cover_letter(job, lang)
    send_email(job, letter_html, lang)
    save_to_sheets(job, lang)
