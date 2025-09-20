import os
import smtplib
from email.message import EmailMessage
from scraper import scrape_all
import openai
import requests

# Variables d'environnement
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
NOTION_API_KEY = os.getenv("NOTION_API_KEY")
NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID")
SMTP_EMAIL = os.getenv("SMTP_EMAIL")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
CV_LINK_FR = os.getenv("CV_LINK_FR")
CV_LINK_ES = os.getenv("CV_LINK_ES")

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
            messages=[{"role": "system", "content": "Tu es un assistant RH expert."},
                      {"role": "user", "content": prompt}],
            max_tokens=300
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"[GPT] Erreur : {e}")
        return ""


# ===========================
# Envoi d'email via Outlook
# ===========================
def send_email(job, letter, language="fr"):
    msg = EmailMessage()
    msg["Subject"] = f"Candidature : {job.get('title')}"
    msg["From"] = SMTP_EMAIL
    msg["To"] = job.get("apply_email", SMTP_EMAIL)  # fallback si pas d'adresse

    # Corps du mail
    msg.set_content(letter)

    # Sélection du CV selon langue
    cv_url = CV_LINK_FR if language == "fr" else CV_LINK_ES
    msg.add_alternative(f"""
    <p>{letter}</p>
    <p>Mon CV est disponible ici : <a href="{cv_url}">Télécharger CV</a></p>
    """, subtype="html")

    try:
        with smtplib.SMTP("smtp.office365.com", 587) as server:
            server.starttls()
            server.login(SMTP_EMAIL, SMTP_PASSWORD)
            server.send_message(msg)
        print(f"📩 Email envoyé pour {job.get('title')} chez {job.get('company')}")
    except Exception as e:
        print(f"[Email] Erreur : {e}")


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
        requests.post(url, headers=headers, json=data)
        print(f"🗂 Offre enregistrée dans Notion ({job.get('title')})")
    except Exception as e:
        print(f"[Notion] Erreur : {e}")


# ===========================
# Détection langue simple
# ===========================
def detect_language(job):
    title = job.get("title", "").lower()
    if any(word in title for word in ["ingeniero", "qa", "pruebas", "automatización", "tecnología"]):
        return "es"
    return "fr"


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

    for i, job in enumerate(jobs[:5], 1):  # ⚠ limite à 5 pour éviter le spam
        print(f"\n--- Offre {i}/{len(jobs)} ---")
        print(f"💼 {job.get('title')} chez {job.get('company')} ({job.get('source')})")

        # Détection de langue
        lang = detect_language(job)

        # Génération lettre de motivation
        letter = generate_cover_letter(job, lang)
        print(f"📝 Lettre générée ({lang.upper()}) :\n{letter[:200]}...\n")

        # Envoi email
        send_email(job, letter, lang)

        # Sauvegarde Notion
        save_to_notion(job, lang)

    print("\n🎯 Processus terminé.")


if __name__ == "__main__":
    main()
