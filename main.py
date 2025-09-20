import os
import smtplib
from email.message import EmailMessage
from email.utils import formataddr
from scraper import scrape_all
import openai
import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import schedule
import time

# ================================
# Variables d'environnement
# ================================
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SMTP_EMAIL = os.getenv("SMTP_EMAIL")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
CV_LINK_FR = os.getenv("CV_LINK_FR")
CV_LINK_ES = os.getenv("CV_LINK_ES")
SHEET_URL = "https://docs.google.com/spreadsheets/d/1Rgd-OuFHA-nXaBPBaZyVlFv7cTsphHScPih4-jn9st8/edit"
IMAGE_URL = "https://image.freepik.com/photos-gratuite/specialiste-informatique-dans-ferme-serveurs-minimisant-defaillances-machines_264385749.jpg"
CREDENTIALS_FILE = "absolute-bonsai-459420-q4-dddac3ebbb21.json"

openai.api_key = OPENAI_API_KEY

# ================================
# Google Sheets setup
# ================================
scope = ["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, scope)
client = gspread.authorize(creds)
sheet = client.open_by_url(SHEET_URL).sheet1

# ================================
# Détection de langue
# ================================
def detect_language(job):
    title = job.get("title","").lower()
    if any(word in title for word in ["ingeniero","qa","pruebas","automatización","tecnología"]):
        return "es"
    return "fr"

# ================================
# Génération lettre HTML
# ================================
def generate_cover_letter(job, language="fr"):
    prompt_fr = f"""
    Tu es un spécialiste IA et RH. Rédige une lettre de motivation courte, percutante et professionnelle pour ce poste :
    Titre : {job.get('title')}
    Entreprise : {job.get('company')}
    Offre : {job.get('url')}
    Le mail doit être en HTML avec mise en page attractive (couleurs, sections, call-to-action)
    et inclure subtilement un lien vers l'image : {IMAGE_URL}
    """
    prompt_es = f"""
    Eres un especialista en IA y RRHH. Escribe una carta de motivación breve, impactante y profesional para este puesto:
    Puesto: {job.get('title')}
    Empresa: {job.get('company')}
    Oferta: {job.get('url')}
    El mail debe estar en HTML con un diseño atractivo (colores, secciones, call-to-action)
    e incluir sutilmente un enlace a la imagen: {IMAGE_URL}
    """
    prompt = prompt_fr if language=="fr" else prompt_es

    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "Tu es un assistant RH expert."},
                      {"role": "user", "content": prompt}],
            max_tokens=500
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"[GPT] Erreur : {e}")
        return "<p>Lettre indisponible</p>"

# ================================
# Envoi email avec HTML + pièces jointes
# ================================
def send_email(job, letter_html, language="fr"):
    msg = EmailMessage()
    msg["Subject"] = f"Candidature : {job.get('title')}"
    msg["From"] = formataddr(("Yacine Bedhouche", SMTP_EMAIL))
    msg["To"] = job.get("apply_email", SMTP_EMAIL)

    msg.add_alternative(letter_html, subtype="html")

    # CV en pièce jointe
    cv_url = CV_LINK_FR if language=="fr" else CV_LINK_ES
    cv_data = requests.get(cv_url).content
    cv_filename = f"CV_Yacine_{language.upper()}.{'pdf' if language=='fr' else 'docx'}"
    msg.add_attachment(cv_data, maintype="application", subtype="octet-stream", filename=cv_filename)

    # Image en pièce jointe
    img_data = requests.get(IMAGE_URL).content
    msg.add_attachment(img_data, maintype="image", subtype="jpeg", filename="image_job.jpg")

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(SMTP_EMAIL, SMTP_PASSWORD)
            server.send_message(msg)
        print(f"📩 Email envoyé pour {job.get('title')} chez {job.get('company')}")
    except Exception as e:
        print(f"[Email] Erreur : {e}")

# ================================
# Sauvegarde Google Sheets
# ================================
def save_to_sheet(job, language):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sheet.append_row([
        job.get("title"),
        job.get("company"),
        job.get("source",""),
        job.get("url"),
        language.upper(),
        now
    ])
    print(f"🗂 Offre enregistrée dans Google Sheets ({job.get('title')})")

# ================================
# Job processing
# ================================
def process_jobs():
    print("🚀 Démarrage du bot de candidature automatique...\n")
    jobs = scrape_all()
    if not jobs:
        print("📭 Aucune offre trouvée.")
        return

    for i, job in enumerate(jobs[:5],1):
        print(f"\n--- Offre {i}/{len(jobs)} ---")
        print(f"💼 {job.get('title')} chez {job.get('company')} ({job.get('source')})")
        lang = detect_language(job)
        letter_html = generate_cover_letter(job, lang)
        send_email(job, letter_html, lang)
        save_to_sheet(job, lang)

    print("\n🎯 Processus terminé.")

# ================================
# Scheduler toutes les heures
# ================================
schedule.every().hour.do(process_jobs)

if __name__=="__main__":
    print("🕒 Scheduler activé : le bot s'exécutera toutes les heures.")
    process_jobs()  # exécution immédiate au démarrage
    while True:
        schedule.run_pending()
        time.sleep(60)
