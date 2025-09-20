import openai
import os

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

def generate_cover_letter_html(job, language, image_url, cv_fr, cv_es):
    prompt_fr = f"""
Rédige une lettre de motivation professionnelle et captivante pour ce poste :
Titre : {job.get('title')}
Entreprise : {job.get('company')}
Offre : {job.get('url')}
Inclure un ton confiant et clair.
"""
    prompt_es = f"""
Escribe una carta de motivación profesional y convincente para este puesto:
Puesto : {job.get('title')}
Empresa : {job.get('company')}
Oferta : {job.get('url')}
Incluye un tono confiado y claro.
"""

    prompt = prompt_fr if language == "fr" else prompt_es

    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "Tu es un assistant RH expert."},
                      {"role": "user", "content": prompt}],
            max_tokens=500
        )
        letter_text = response.choices[0].message.content.strip()
    except Exception as e:
        print(f"[GPT] Erreur : {e}")
        letter_text = "Veuillez afficher cette lettre en HTML."

    cv_link = cv_fr if language=="fr" else cv_es

    html = f"""
<html>
<body>
<img src="{image_url}" style="width:100%;max-width:600px;margin-bottom:20px;">
<p>{letter_text}</p>
<p>Télécharger mon CV : <a href="{cv_link}">ici</a></p>
</body>
</html>
"""
    return html
