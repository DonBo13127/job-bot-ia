import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_cover_letter_html(job, language, image_url, cv_fr, cv_es):
    prompt_fr = f"""
    Rédige une lettre de motivation courte et professionnelle pour ce poste en français :
    {job.get('title')} chez {job.get('company')}
    """
    prompt_es = f"""
    Redacta una carta de motivación breve y profesional para este puesto en español:
    {job.get('title')} en {job.get('company')}
    """

    prompt = prompt_fr if language=="fr" else prompt_es

    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role":"system","content":"Tu es un assistant RH expert."},
            {"role":"user","content":prompt}
        ],
        max_tokens=300
    )

    letter = response.choices[0].message.content.strip()
    cv_link = cv_fr if language=="fr" else cv_es

    html = f"""
    <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.5; color: #333;">
            <img src="{image_url}" alt="AI Specialist" style="max-width:100%; height:auto; margin-bottom:20px;">
            <p>{letter}</p>
            <p>Mon CV est attaché en pièce jointe ou téléchargeable ici : <a href="{cv_link}">Télécharger CV</a></p>
        </body>
    </html>
    """
    return html
