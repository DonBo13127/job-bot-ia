import os
import smtplib
from email.message import EmailMessage
from scraper import scrape_all
import openai
import requests
from langdetect import detect
import tempfile
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed

# ===========================
# Variables d'environnement
# ===========================
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
NOTION_API_KEY = os.getenv("NOTION_API_KEY")
NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID")
SMTP_EMAIL = os.getenv("SMTP_EMAIL")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
CV_LINK_FR = os.getenv("CV_LINK_FR")
CV_LINK_ES = os.getenv("CV_LINK_ES")
MAX_EMAILS_PER_RUN = 5  # Limite journalier configurable

openai.api_key = OPENAI_API_KEY

# ===========================
# Génération de la candidature
# ===========================
def generate_cover_letter(job, language="fr"):
    prompt_fr = f"""
    Rédige une lettre de motivation courte et professionnelle pour postuler à ce poste :
    Titre : {job.get('title')}
    Entreprise : {job.get('company')}
    Offre : {job.get('url')}
    """
    prompt_es = f"""
    Escribe una carta de motivación breve y profesional para postular a este puesto:
    Puesto: {job.get('title')}
    Empresa: {job.get('company')}
    Oferta: {job.get('url')}
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
# Détection automatique de langue
# ===========================
def detect_language(job):
    try:
        return "es" if detect(job.get("title", "") + " " + job.get("description", "")) == "es" else "fr"
    except:
        return "fr"

# ===========================
# Télécharger un fichier temporaire
# ===========================
def download_cv(url):
    tmp_file = tempfile.NamedTemporaryFile(delete=False)
    urllib.request.urlretrieve(url, tmp_file.name)
    return tmp_file.name

# ===========================
# Envoi d'email via Outlook
# ===========================
def send_email(job, letter, language="fr"):
    msg = EmailMessage()
    msg["Subject"] = f"Candidature : {job.get('title')}"
    msg["From"] = SMTP_EMAIL
    msg["To"] = job.get("apply_email") or SMTP_EMAIL  # fallback

    msg.set_content(letter)

    # CV attaché
    cv_url = CV_LINK_FR if language == "fr" else CV_LINK_ES
    cv_file = download_cv(cv_url)
    filename = "CV-FR.pdf" if language == "fr" else "CV-ES.docx"
    with open(cv_file, "rb") as f:
        msg.add_attachment(f.read(), maintype="application", subtype="octet-stream", filename=filename)

    try:
        with smtplib.SMTP("smtp.office365.com", 587) as server:
            server.starttls()
            server.login(SMTP_EMAIL, SMTP_PASSWORD)
            server.send_message(msg)
        print(f"📩 Email envoyé pour {job.get('title')} chez {job.get('company')}")
    except Exception as e:
        print(f"[Email] Erreur : {e}")

# ===========================
# Vérifie si l'offre existe déjà dans Notion
# ===========================
def job_exists_in_notion(job_url):
    url = f"https://api.notion.com/v1/databases/{NOTION_DATABASE_ID}/query"
    headers = {
        "Authorization": f"Bearer {NOTION_API_KEY}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }
    query = {"filter": {"property": "URL", "url": {"equals": job_url}}}
    try:
        response = requests.post(url, headers=headers, json=query)
        if response.status_code == 200:
            results = response.json().get("results", [])
            return len(results) > 0
        else:
            print(f"[Notion] Erreur lors de la vérification : {response.status_code}")
            return False
    except Exception as e:
        print(f"[Notion] Exception vérification : {e}")
        return False

# ===========================
# Sauvegarde dans Notion
# ===========================
def save_to_notion(job, language):
    url = "https://api.notion.com/v1/pages"
    headers = {
        "Authorization": f"Bearer {NOTION_API_KEY}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }
    data = {
        "parent": {"database_id": NOTION_DATABASE_ID},
        "properties": {
            "Titre": {"title": [{"text": {"content": job.get("title", "Sans titre")}}]},
            "Entreprise": {"rich_text": [{"text": {"content": job.get("company", "Inconnue")}}]},
            "Source": {"rich_text": [{"text": {"content": job.get("source", "N/A")}}]},
            "URL": {"url": job.get("url", "")},
            "Langue CV": {"rich_text": [{"text": {"content": language.upper()}}]}
        }
    }
    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code in [200, 201]:
            print(f"🗂 Offre enregistrée dans Notion ({job.get('title')})")
        else:
            print(f"[Notion] Erreur {response.status_code} : {response.text}")
    except Exception as e:
        print(f"[Notion] Exception : {e}")

# ===========================
# Processus pour une offre
# ===========================
def process_job(job):
    if job_exists_in_notion(job.get("url")):
        print(f"⚠ Offre déjà traitée : {job.get('title')}")
        return

    lang = detect_language(job)
    letter = generate_cover_letter(job, lang)
    send_email(job, letter, lang)
    save_to_notion(job, lang)

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
    jobs_to_process = jobs[:MAX_EMAILS_PER_RUN]

    # Multithreading
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(process_job, job) for job in jobs_to_process]
        for future in as_completed(futures):
            future.result()

    print("\n🎯 Processus terminé.")

if __name__ == "__main__":
    main()
