# main.py
from scraper import scrape_all
from notion_db import NotionDB
from gpt_generator import generate_cover_letter
from email_sender import send_email
import requests
import re
import time
import os


def extract_email_from_text(text):
    """
    Extrait les emails valides et filtre les génériques
    """
    emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b', text)
    # Filtre les emails non pertinents
    blocked_keywords = ['noreply', 'no-reply', 'donotreply', 'contact', 'info', 'hello', 'support', 'admin', 'jobs', 'career']
    valid_emails = [
        email for email in emails
        if not any(bad in email.lower() for bad in blocked_keywords)
    ]
    return valid_emails[0] if valid_emails else None


def extract_contact_from_job_page(job_url):
    """
    Télécharge la page de l'offre et extrait un email pertinent
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"
    }
    try:
        r = requests.get(job_url, headers=headers, timeout=12)
        r.raise_for_status()
        return extract_email_from_text(r.text)
    except Exception as e:
        print(f"[Email Extract] Impossible de charger {job_url} : {e}")
        return None


def main():
    print("🚀 Démarrage du bot de candidature automatique...\n")

    # Initialisation
    db = NotionDB()

    # Étape 1 : Scraping
    print("🔍 Collecte des offres d'emploi...")
    all_jobs = scrape_all()
    print(f"✅ {len(all_jobs)} offres collectées.\n")

    if not all_jobs:
        print("📭 Aucune offre trouvée. Fin du processus.")
        return

    # Étape 2 : Traitement une par une
    for idx, job in enumerate(all_jobs, start=1):
        print(f"\n--- Offre {idx}/{len(all_jobs)} ---")
        print(f"💼 {job['title']} chez {job['company']} ({job['site'].upper()})")

        # Vérifier si déjà traité
        if db.job_exists(job['url']):
            print("🔁 [Doublon] Offre déjà traitée. Ignorée.")
            continue

        # Extraire un email de contact
        print("📧 Recherche d'email de contact...")
        contact_email = extract_contact_from_job_page(job['url'])
        if not contact_email:
            print("❌ Aucun email trouvé. Ignorée.")
            continue
        print(f"📩 Email trouvé : {contact_email}")

        # Générer la lettre de motivation
        print("✍️ Génération de la lettre de motivation...")
        cover_letter = generate_cover_letter(
            job_title=job['title'],
            company=job['company'],
            language=job.get('language', 'fr')
        )

        # Préparer l'email
        subject = f"Candidature spontanée – {job['title']}"
        cv_link = os.getenv("CV_LINK_FR") if job.get('language', 'fr') == 'fr' else os.getenv("CV_LINK_ES")
        body = f"""
Bonjour,

{cover_letter}

Vous trouverez mon CV ici : {cv_link}

Disponible immédiatement en full remote. Je serais ravi d’échanger sur les besoins de votre équipe en matière d’automatisation, de scraping ou d’agents IA.

Cordialement,
Yacine Bedhouche
---
📧 yacine.bedhouche@protonmail.com
🔗 linkedin.com/in/votreprofil (optionnel)
"""

        # Envoyer l'email
        print(f"📤 Envoi à {contact_email}...")
        if send_email(to_email=contact_email, subject=subject, body=body.strip()):
            print("✅ Candidature envoyée !")
            # Enregistrer dans Notion
            db.add_job({
                "title": job['title'],
                "company": job['company'],
                "url": job['url'],
                "location": job['location'],
                "language": job.get('language', 'fr'),
                "date_posted": time.strftime("%Y-%m-%d"),
                "site": job['site']
            })
        else:
            print("❌ Échec de l'envoi.")

        # Pause anti-spam
        time.sleep(7)

    print("\n🎉 Processus terminé. Le bot a fini son travail.")


if __name__ == "__main__":
    main()
