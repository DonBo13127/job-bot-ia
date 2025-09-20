import openai
import os

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

def generate_cover_letter_html(job, language="fr", image_url=None):
    prompt_fr = f"""
Rédige une lettre de motivation professionnelle courte pour postuler à ce poste :
Titre : {job.get('title')}
Entreprise : {job.get('company')}
Offre : {job.get('url')}
Utilise un ton dynamique et engageant, en mettant en avant mes compétences en IA.
"""
    prompt_es = f"""
Escribe una carta de motivación breve y profesional para postular a este puesto:
Puesto: {job.get('title')}
Empresa: {job.get('company')}
Oferta: {job.get('url')}
Utiliza un tono dinámico y resalta mis habilidades en IA.
"""
    prompt = prompt_fr if language == "fr" else prompt_es

    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role":"system","content":"Tu es un expert RH et copywriter."},
                      {"role":"user","content":prompt}],
            max_tokens=500
        )
        letter = response.choices[0].message.content.strip()
    except Exception as e:
        print(f"[GPT] Erreur : {e}")
        letter = "Bonjour,\nJe souhaite postuler à cette offre."

    # Création HTML avec image
    html = f"""
    <html>
    <body style="font-family: Arial, sans-serif; line-height:1.5; color:#333;">
        <h2 style="color:#2E86C1;">Candidature : {job.get('title')}</h2>
        <h3>{job.get('company')}</h3>
        <img src="{image_url}" alt="Image" style="max-width:600px; margin:15px 0;">
        <p>{letter}</p>
        <p>CV en pièce jointe.</p>
    </body>
    </html>
    """
    return html
