import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_cover_letter_html(job, lang, image_url, cv_link_fr, cv_link_es):
    title = job.get("title")
    company = job.get("company")
    url = job.get("link")

    prompt = f"""
    Rédige une lettre de motivation professionnelle et chaleureuse pour postuler à ce poste.
    Poste: {title}
    Entreprise: {company}
    Lien de l'offre: {url}
    Langue: {lang}
    """

    if lang == "es":
        prompt = prompt.replace("Rédige", "Escribe").replace("professionnelle et chaleureuse", "profesional y cordial")

    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=400
        )
        letter_text = response.choices[0].message.content.strip()
    except Exception as e:
        print(f"[GPT] Erreur : {e}")
        letter_text = "Bonjour, je souhaite postuler à votre offre."

    cv_link = cv_link_fr if lang == "fr" else cv_link_es

    html_content = f"""
    <html>
    <body>
        <img src="{image_url}" style="max-width:600px;"><br><br>
        <p>{letter_text}</p>
        <p>Mon CV en pièce jointe ou téléchargeable ici : <a href="{cv_link}">Télécharger CV</a></p>
    </body>
    </html>
    """
    return html_content
