# gpt_generator.py
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_cover_letter(job_title, company, language="fr"):
    prompt = f"""
    Rédige une lettre de motivation courte et percutante en {'français' if language == 'fr' else 'espagnol'} pour le poste de {job_title} chez {company}.
    Mets en avant :
    - Mon expertise en automatisation, scraping, agents IA
    - Mon expérience en test logiciel (ISTQB)
    - Mon profil autonome, orienté solutions
    - Disponibilité immédiate, full remote
    Style : professionnel mais moderne, max 150 mots.
    Termine par une formule de politesse.
    """
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300
    )
    return response.choices[0].message.content.strip()
