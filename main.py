import os
import smtplib
from email.message import EmailMessage
from langdetect import detect
import openai
import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from scraper import scrape_all
from datetime import datetime

# ===========================
# Variables d'environnement
# ===========================
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SMTP_EMAIL = os.getenv("SMTP_EMAIL")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
CV_LINK_FR = os.getenv("CV_LINK_FR")
CV_LINK_ES = os.getenv("CV_LINK_ES")
SHEET_NAME = "Job Applications"  # Nom de ton Google Sheet
CREDENTIALS_FILE = "absolute-bonsai-459420-q4-dddac3ebbb21.json"  # Ton JSON

openai.api_key = OPENAI_API_KEY

# ===========================
# Connexion Google Sheets
# ===========================
scope = ["https://spreadsheets.google.com/feeds",
         "https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, scope)
client = gspread.authorize(creds)
sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1Rgd-OuFHA-nXaBPBaZyVlFv7cTsphHScPih4-jn9st8/edit").sheet1

# ===========================
# Détection de langue
# ===========================
def detect_language(job):
    title = job.get("title", "").lower()
    if any(word in title for word in ["ingeniero", "qa", "pruebas", "automatización", "tecnología"]):
        return "es"
    return "fr"

# ===========================
# Génération lettre de motivation
# ===========================
def generate_cover_letter(job, language="fr"):
    prompt_fr = f"""
Rédige une lettre de motivation courte et professionnelle pour postuler à ce poste :
Titre : {job.get('title')}
Entreprise : {job.get('company')}
Offre : {job.get('url')}
Inclue une image illustrant un spécialiste informatique : https://fr.freepik.com/photos-gratuite/specialiste-informatique-dans-ferme-serveurs-minimisant-defaillances-machines_264385749.htm#fromView=search&page=1&position=5&uuid=f6600eb9-89a4-4b30-94a2-d917bd260646&query=IT
"""

    prompt_es = f"""
Escribe una carta de motivación breve y profesional para postular a este puesto:
Puesto: {job.get('title')}
Empresa: {job.get('company')}
Oferta: {job.get('url')}
Incluye una imagen que ilustre a un especialista en informática: https://fr.freepik.com/photos-gratuite/specialiste-informatique-dans-ferme-serveurs-minimisant-defaillances-machines_264385749.htm#fromView=search&page=1&position=5&uuid=f6600eb9-89a4-4b30-94a2-d917bd260646&query=IT
"""

    prompt = prompt_fr if language == "fr" else prompt_es

    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Tu es un assistant RH expert."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300
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

    msg.set_content(letter)
    cv_url = CV_LINK_FR if language == "fr" else CV_LINK_ES
    msg.add_alternative(f"""
<p>{letter}</p>
<p>Mon CV est disponible ici : <a href="{cv_url}">Télécharger CV</a></p>
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
# Sauvegarde dans Google Sheets
# ===========================
def save_to_sheet(job, language):
    try:
        # Vérifie doublon
        records = sheet.get_all_records()
        urls = [r.get("URL", "") for r in records]
        if job.get("url") in urls:
            print(f"⚠ Offre déjà sauvegardée : {job.get('title')}")
            return
        # Ajout
        sheet.append_row([
            job.get("title", ""),
            job.get("company", ""),
            job.get("source", ""),
            job.get("url", ""),
            language.upper(),
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ])
        print(f"🗂 Offre sauvegardée : {job.get('title')}")
    except Exception as e:
        print(f"[Sheets] Erreur : {e}")

# ===========================
# Main
# ===========================
def main():
    print("🚀 Démarrage du bot de candidature automatique...\n")
    jobs = scrape_all()
    if not jobs:
        print("📭 Aucune offre trouvée.")
        return

    print(f"✅ {len(jobs)} offres collectées.\n")

    for i, job in enumerate(jobs[:5], 1):  # limite à 5 pour éviter le spam
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
