import openai

openai.api_key = "TON_OPENAI_API_KEY"

def generate_cover_letter_html(job_title, company, lang="fr", image_url=None):
    prompt = f"""
    Rédige une lettre de motivation en HTML pour postuler au poste '{job_title}' chez '{company}'.
    La lettre doit être adaptée à la langue {lang} et inclure l'image suivante : {image_url}.
    Mets en page la lettre de façon professionnelle et attrayante.
    """
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role":"user","content":prompt}],
        max_tokens=700
    )
    return response.choices[0].message.content
