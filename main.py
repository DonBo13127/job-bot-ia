import os
import smtplib
from email.message import EmailMessage
from langdetect import detect
import openai
import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from scraper import scrape_all  # ton scraper existant

# ===========================
# Variables d'environnement
# ===========================
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SMTP_EMAIL = os.getenv("SMTP_EMAIL")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
CV_LINK_FR = os.getenv("CV_LINK_FR")
CV_LINK_ES = os.getenv("CV_LINK_ES")
CREDENTIALS_FILE = "absolute-bonsai-459420-q4-dddac3ebbb21.json"
GOOGLE_SHEET_KEY = "1Rgd-OuFHA-nXaBPBaZyVlFv7cTsphHScPih4-jn9st8"

# API Key
openai.api_key = OPENAI_API_KEY

# ===========================
# Connexion Google Sheets
# ===========================
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, scope)
client = gspread.authorize(creds)
sheet = client.open_by_key(GOOGLE_SHEET_KEY).sheet1

# ===========================
# Fonctions
# ===========================
def detect_language(job):
    title = job.get("title", "").lower()
    if any(word in title for word in ["ingeniero", "pruebas", "automatización", "tecnología"]):
        return "es"
    return "fr"

def generate_cover_letter(job, language="fr"):
    image_url = "https://img.freepik.com/photos-gratuite/specialiste-informatique-dans-ferme-serveurs-minimisant-defaillances-machines_264385749.jpg"
    if language == "fr":
        prompt = f"""
        Tu es un spécialiste en IA et RH. Rédige une lettre de motivation concise, professionnelle & percutante :
        Titre : {job.get('title')}
        Entreprise : {job.get('company')}
        Offre : {job.get('url')}
        Inclure une image visuelle : {image_url}
        Mets en avant expérience ISTQB, automatisation, IA, optimisation et qualité logicielle.
        """
    else:
        prompt = f"""
        Eres especialista en IA y RH. Escribe una carta de motivación breve, profesional y convincente:
        Puesto: {job.get('title')}
        Empresa: {job.get('company')}
        Oferta: {job.get('url')}
        Incluye imagen visual : {image_url}
        Destaca experiencia ISTQB, automatización, IA, optimización y calidad de software.
        """
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Tu es un assistant RH expert et spécialiste IA."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=400
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"[GPT] Erreur : {e}")
        return ""

def send_email(job, letter, language="fr"):
    msg = EmailMessage()
    msg["Subject"] = f"Candidature : {job.get('title')}"
    msg["From"] = SMTP_EMAIL
    msg["To"] = job.get("apply_email", SMTP_EMAIL)  # fallback

    # version texte
    msg.set_content(letter)
    # version HTML avec image et lien CV
    cv_url = CV_LINK_FR if language == "fr" else CV_LINK_ES
    msg.add_alternative(f"""
    <html>
      <body>
        <p>{letter}</p>
        <p>Mon CV : <a href="{cv_url}">Télécharger CV</a></p>
        <p><img src="https://img.freepik.com/photos-gratuite/specialiste-informatique-dans-ferme-serveurs-minimisant-defaillances-machines_264385749.jpg" alt="Image IA" width="400"></p>
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

def exists_in_sheet(job):
    try:
        records = sheet.get_all_records()
        # suppose que tu as une colonne "URL" dans ton sheet
        return any(r.get("URL", "") == job.get("url") for r in records)
    except Exception as e:
        print(f"[Sheets] Erreur lecture : {e}")
        return False

def save_to_sheet(job, language):
    if exists_in_sheet(job):
        print(f"⚠ Offre déjà enregistrée : {job.get('title')}")
        return
    sheet.append_row([
        job.get("title", ""),
        job.get("company", ""),
        job.get("source", ""),
        job.get("url", ""),
        language.upper(),
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ])
    print(f"🗂 Offre sauvegardée : {job.get('title')}")

def main():
    from datetime import datetime
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
        send_email(job, letter, lang)
        save_to_sheet(job, lang)
    print("\n🎯 Processus terminé.")

if __name__ == "__main__":
    main()
