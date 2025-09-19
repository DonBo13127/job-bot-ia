# main.py
from scraper import scrape_wttj
from notion_db import NotionDB
from gpt_generator import generate_cover_letter
from email_sender import send_email
import time
import os

def extract_contact_from_job_page(job_url):
    """Extrait un email depuis la page détaillée de l'offre"""
    try:
        r = requests.get(job_url, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(r.text, 'html.parser')
        text = soup.get_text()
        import re
        emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
        for email in emails:
            if "mailto:" not in email and "noreply" not in email and "admin" not in email:
                return email
        return None
    except:
        return None

def main():
    db = NotionDB()
    jobs = scrape_wttj()  # Ajouter d'autres scrapers ici

    for job in jobs:
        if db.job_exists(job['url']):
            print(f"[Doublon] Ignoré : {job['title']}")
            continue

        contact_email = extract_contact_from_job_page(job['url'])
        if not contact_email:
            print(f"[Sans email] Ignoré : {job['title']}")
            continue

        cover_letter = generate_cover_letter(job['title'], job['company'], job['language'])
        subject = f"Candidature au poste : {job['title']}"

        cv_link = os.getenv("CV_LINK_FR") if job['language'] == 'fr' else os.getenv("CV_LINK_ES")
        body = f"""
Bonjour,

{cover_letter}

Mon CV est disponible ici : {cv_link}

Disponible immédiatement en full remote.

Cordialement,
Yacine Bedhouche
"""

        if send_email(contact_email, subject, body):
            db.add_job(job)
        time.sleep(5)  # Anti-spam

if __name__ == "__main__":
    main()
