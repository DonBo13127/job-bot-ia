import openai

openai.api_key = "TON_OPENAI_API_KEY"

def generate_cover_letter_html(job_title, company, lang="fr", image_url=None):
    prompt = f"""
    Rédige une lettre de motivation professionnelle en HTML pour postuler au poste '{job_title}' chez '{company}'.
    La lettre doit être en {lang}, inclure l'image suivante {image_url} et avoir une mise en page attrayante.
    """
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=700
    )
    return response.choices[0].message.content
