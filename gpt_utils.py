import openai
import os

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

IMAGE_URL = "https://img.freepik.com/photos-gratuite/specialiste-informatique-dans-ferme-serveurs-minimisant-defaillances-machines_264385749.htm"

CV_LINK_FR = os.getenv("CV_LINK_FR")
CV_LINK_ES = os.getenv("CV_LINK_ES")

def generate_cover_letter_html(job, language="fr"):
    prompt = f"""
Rédige une lettre de motivation professionnelle et convaincante pour postuler au poste suivant :
Titre : {job.get('title')}
Entreprise : {job.get('company')}
URL de l'offre : {job.get('url')}
Langue : {language}
"""
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Tu es un expert RH et copywriter."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=400
        )
        letter = response.choices[0].message.content.strip()
    except Exception as e:
        print(f"[GPT] Erreur : {e}")
        letter = "Bonjour, je souhaite postuler pour ce poste."

    cv_link = CV_LINK_FR if language == "fr" else CV_LINK_ES

    html_content = f"""
<html>
<body>
    <p>{letter}</p>
    <p>Mon CV : <a href="{cv_link}">Télécharger</a></p>
    <img src="{IMAGE_URL}" alt="Image IA" width="400"/>
</body>
</html>
"""
    return html_content
