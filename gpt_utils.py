import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")
CV_LINK_FR = os.getenv("CV_LINK_FR")
CV_LINK_ES = os.getenv("CV_LINK_ES")
IMAGE_URL = "https://image.freepik.com/photos-gratuite/specialiste-informatique-dans-ferme-serveurs-minimisant-defaillances-machines_264385749.htm"

def generate_cover_letter_html(job, language="fr"):
    prompt = f"""
    Rédige une lettre de motivation courte et professionnelle en mettant en avant les skills essentiels au job sélectionné pour postuler à ce poste :
    Titre : {job['title']}
    Entreprise : {job['company']}
    Offre : {job['url']}
    Langue : {language}
    """
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role":"system","content":"Tu es un expert RH et copywriter."},
                  {"role":"user","content":prompt}],
        max_tokens=400
    )
    letter_text = response.choices[0].message.content.strip()

    cv_url = CV_LINK_FR if language=="fr" else CV_LINK_ES
    html = f"""
    <html>
    <body>
        <p>{letter_text}</p>
        <p><img src="{IMAGE_URL}" alt="IA" width="600"/></p>
        <p>CV en pièce jointe : <a href="{cv_url}">Télécharger CV</a></p>
    </body>
    </html>
    """
    return html
