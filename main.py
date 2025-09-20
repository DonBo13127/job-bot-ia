import os
import smtplib
from email.message import EmailMessage
from datetime import datetime
import schedule
import time
from scraper import scrape_all_ai
from gpt_utils import generate_cover_letter_html
from sheets_utils import connect_sheets, save_job

# ===========================
# Variables d'environnement
# ===========================
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SMTP_EMAIL = os.getenv("SMTP_EMAIL")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
CV_LINK_FR = os.getenv("CV_LINK_FR")
CV_LINK_ES = os.getenv("CV_LINK_ES")
IMAGE_URL = "https://img.freepik.com/photos-gratuite/specialiste-informatique-dans-ferme-serveurs-minimisant-defaillances-machines_264385749.jpg"

SHEET_JSON = "absolute-bonsai-459420-q4-dddac3ebbb21.json"
SHEET_NAME = "Replit"

# ===========================
# Connexion Google Sheets
# ===========================
sheet = connect_sheets(SHEET_JSON, SHEET_NAME)

# ===========================
# Envoi email via Gmail
# ===========================
def send_email(job, letter_html, language="fr"):
    recipient = job.get("apply_email")
    if not recipient:
        print(f"[Email] Aucun destinataire pour {job.get('title')}")
        return

    msg = EmailMessage()
    msg["Subject"] = f"Candidature : {job.get('title')}"
    msg["From"] = SMTP_EMAIL
    msg["To"] = recipient

    # Ajouter HTML
    msg.add_alternative(letter_html, subtype="html")

    # Ajouter CV en pièce jointe
    cv_link = CV_LINK_FR if language == "fr" else CV_LINK_ES
    try:
        import requests
        cv_data = requests.get(cv_link).content
        msg.add_attachment(cv_data, maintype="application", subtype="pdf", filename=f"CV-{language.upper()}.pdf")
    except Exception as e:
        print(f"[Email] Erreur téléchargement CV : {e}")

    # Ajouter image en pièce jointe
    try:
        img_data = requests.get(IMAGE_URL).content
        msg.add_attachment(img_data, maintype="image", subtype="jpeg", filename="image.jpg")
    except Exception as e:
        print(f"[Email] Erreur téléchargement image : {e}")

    # Envoi via SMTP Gmail
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(SMTP_EMAIL, SMTP_PASSWORD)
            server.send_message(msg)
        print(f"📩 Email envoyé à {recipient} pour {job.get('title')}")
    except Exception as e:
        print(f"[Email] Erreur : {e}")

# ===========================
# Fonction principale
# ===========================
def main():
    print(f"\n🚀 Démarrage du bot de candidature automatique {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ...")

    jobs = scrape_all_ai()
    if not jobs:
        print("📭 Aucune offre IA trouvée.")
        return

    print(f"✅ {len(jobs)} offres IA collectées.\n")

    for i, job in enumerate(jobs[:5], 1):  # limiter pour tests
        print(f"\n--- Offre {i}/{len(jobs)} ---")
        print(f"💼 {job.get('title')} chez {job.get('company')} ({job.get('source')})")

        # Détection langue
        lang = "es" if any(word in job.get("title", "").lower() for word in ["ingeniero", "automatización"]) else "fr"

        # Génération lettre HTML
        letter_html = generate_cover_letter_html(job, lang, IMAGE_URL)

        # Envoi email
        send_email(job, letter_html, lang)

        # Sauvegarde Google Sheets
        save_job(sheet, job, lang)

    print("🎯 Processus terminé.\n")

# ===========================
# Scheduler toutes les heures
# ===========================
schedule.every().hour.do(main)
print("🕒 Scheduler activé : le bot s'exécutera toutes les heures.")

while True:
    schedule.run_pending()
    time.sleep(60)
