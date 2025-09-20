import os
import smtplib
from email.message import EmailMessage
from scraper import scrape_all
import openai
import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime  # ✅ Ajouté pour l'erreur datetime

# Variables d'environnement
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SMTP_EMAIL = os.getenv("SMTP_EMAIL")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
CV_LINK_FR = os.getenv("CV_LINK_FR")
CV_LINK_ES = os.getenv("CV_LINK_ES")
SHEET_NAME = "Job Applications"

# Google Sheets
CREDENTIALS_FILE = "absolute-bonsai-459420-q4-dddac3ebbb21.json"
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, scope)
client = gspread.authorize(creds)
sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1Rgd-OuFHA-nXaBPBaZyVlFv7cTsphHScPih4-jn9st8/edit").sheet1

openai.api_key = OPENAI_API_KEY

# ===========================
# Détection de langue simple
# ===========================
def detect_language(job):
    title = job.get("title", "").lower()
    if any(word in title for word in ["ingeniero", "qa", "pruebas", "automatización", "tecnología"]):
        return "es"
    return "fr"

# ===========================
# Génération lettre + image
# ===========================
def generate_cover_letter(job, language="fr"):
    prompt_fr = f"""
    Tu es un spécialiste IA et RH. Rédige une lettre de motivation courte, percutante et professionnelle pour ce poste :
    Titre : {job.get('title')}
    Entreprise : {job.get('company')}
    Offre : {job.get('url')}
    Inclue subtilement un lien vers l'image suivante : 
    https://www.freepik.com/photos-gratuite/specialiste-informatique-dans-ferme-serveurs-minimisant-defaillances-machines_264385749.htm
    """
    prompt_es = f"""
    Eres un especialista en IA y RRHH. Escribe una carta de motivación breve, impactante y profesional para este puesto:
    Puesto: {job.get('title')}
    Empresa: {job.get('company')}
    Oferta: {job.get('url')}
    Incluye sutilmente un enlace a esta imagen:
    https://www.freepik.com/photos-gratuite/specialiste-informatique-dans-ferme-serveurs-minimisant-defaillances-machines_264385749.htm
    """
    prompt = prompt_fr if language == "fr" else prompt_es

    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "Tu es un assistant RH expert."},
                      {"role": "user", "content": prompt}],
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
# Sauvegarde Google Sheets
# ===========================
def save_to_sheet(job, language):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sheet.append_row([
        job.get("title"),
        job.get("company"),
        job.get("source", ""),
        job.get("url"),
        language.upper(),
        now
    ])
    print(f"🗂 Offre enregistrée dans Google Sheets ({job.get('title')})")

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
