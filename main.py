import os
import smtplib
from email.message import EmailMessage
from datetime import datetime
import requests
import openai
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from langdetect import detect

# ===========================
# Variables d'environnement
# ===========================
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SMTP_EMAIL = os.getenv("SMTP_EMAIL")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")  # mot de passe d'application Gmail
CV_LINK_FR = os.getenv("CV_LINK_FR")
CV_LINK_ES = os.getenv("CV_LINK_ES")
GOOGLE_SHEET_ID = os.getenv("GOOGLE_SHEET_ID")  # ID du sheet
CREDENTIALS_FILE = "replit_credentials.json"  # fichier JSON du service account

openai.api_key = OPENAI_API_KEY

# ===========================
# Connexion Google Sheets
# ===========================
scope = ["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, scope)
client = gspread.authorize(creds)
sheet = client.open_by_key(GOOGLE_SHEET_ID).sheet1

def already_applied(job_url):
    urls = sheet.col_values(4)
    return job_url in urls

def save_to_sheet(job, language):
    if already_applied(job.get("url")):
        print(f"⚠ Offre déjà postée : {job.get('title')} chez {job.get('company')}")
        return
    row = [
        job.get("title", ""),
        job.get("company", ""),
        job.get("source", ""),
        job.get("url", ""),
        language.upper(),
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ]
    sheet.append_row(row)
    print(f"✅ Offre enregistrée dans Google Sheets ({job.get('title')})")

# ===========================
# Détection langue
# ===========================
def detect_language(job):
    try:
        lang = detect(job.get("title", ""))
        if lang.startswith("es"):
            return "es"
        return "fr"
    except:
        return "fr"

# ===========================
# Génération lettre motivation
# ===========================
def generate_cover_letter(job, language="fr"):
    image_url = "https://image.freepik.com/photos-gratuite/specialiste-informatique-dans-ferme-serveurs-minimisant-defaillances-machines_264385749.htm"

    prompt_fr = f"""
    Tu es un spécialiste en QA et IA. Rédige une lettre de motivation courte et très professionnelle pour postuler à ce poste :
    Titre : {job.get('title')}
    Entreprise : {job.get('company')}
    Offre : {job.get('url')}
    Ajoute cette image au corps du mail : {image_url}
    """
    prompt_es = f"""
    Eres un especialista en QA e IA. Escribe una carta de motivación breve y muy profesional para postular a este puesto:
    Puesto: {job.get('title')}
    Empresa: {job.get('company')}
    Oferta: {job.get('url')}
    Incluye esta imagen en el correo: {image_url}
    """
    prompt = prompt_fr if language == "fr" else prompt_es

    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Tu es un assistant RH expert."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=400
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"[GPT] Erreur : {e}")
        return ""

# ===========================
# Envoi email via Gmail
# ===========================
def send_email(job, letter, language="fr"):
    msg = EmailMessage()
    msg["Subject"] = f"Candidature : {job.get('title')}"
    msg["From"] = SMTP_EMAIL
    msg["To"] = job.get("apply_email", SMTP_EMAIL)

    cv_url = CV_LINK_FR if language == "fr" else CV_LINK_ES

    msg.add_alternative(f"""
    <html>
    <body>
        <p>{letter}</p>
        <p><img src="https://image.freepik.com/photos-gratuite/specialiste-informatique-dans-ferme-serveurs-minimisant-defaillances-machines_264385749.htm" alt="IT Specialist" width="400"/></p>
        <p>Mon CV est disponible ici : <a href="{cv_url}">Télécharger CV</a></p>
    </body>
    </html>
    """, subtype="html")

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(SMTP_EMAIL, SMTP_PASSWORD)
            server.send_message(msg)
        print(f"📩 Email envoyé pour {job.get('title')} chez {job.get('company')}")
    except Exception as e:
        print(f"[Email] Erreur : {e}")

# ===========================
# Main
# ===========================
def main():
    from scraper import scrape_all
    print("🚀 Démarrage du bot de candidature automatique...\n")

    jobs = scrape_all()
    if not jobs:
        print("📭 Aucune offre trouvée.")
        return

    print(f"✅ {len(jobs)} offres collectées.\n")

    for i, job in enumerate(jobs[:5], 1):
        print(f"\n--- Offre {i}/{len(jobs)} ---")
        print(f"💼 {job.get('title')} chez {job.get('company')} ({job.get('source')})")

        lang = detect_language(job)
        letter = generate_cover_letter(job, lang)
        print(f"📝 Lettre générée ({lang.upper()}) :\n{letter[:200]}...\n")

        send_email(job, letter, lang)
        save_to_sheet(job, lang)

    print("\n🎯 Processus terminé.")

if __name__ == "__main__":
    main()
