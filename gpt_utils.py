import openai

def generate_cover_letter_html(job, language="fr"):
    """
    Génère une lettre de motivation en HTML avec mise en page pro, image et lien CV
    """
    prompt_fr = f"""
    Tu es un expert RH et IA. Rédige une lettre de motivation courte,
    professionnelle et attrayante en HTML pour ce poste :
    Titre : {job.get('title')}
    Entreprise : {job.get('company')}
    Offre : {job.get('url')}
    Inclue une mise en page élégante et professionnelle,
    mets en avant les compétences IA et insère une image illustrative :
    https://img.freepik.com/photos-gratuite/specialiste-informatique-dans-ferme-serveurs-minimisant-defaillances-machines_264385749.htm
    """
    
    prompt_es = f"""
    Eres un experto en RRHH e IA. Redacta una carta de motivación corta,
    profesional y atractiva en HTML para este puesto:
    Puesto: {job.get('title')}
    Empresa: {job.get('company')}
    Oferta: {job.get('url')}
    Incluye un diseño elegante y profesional,
    destaca habilidades en IA e incluye esta imagen:
    https://img.freepik.com/photos-gratuite/specialiste-informatique-dans-ferme-serveurs-minimisant-defaillances-machines_264385749.htm
    """

    prompt = prompt_fr if language == "fr" else prompt_es

    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Tu es un assistant RH expert et designer de mail HTML."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500
        )
        html_content = response.choices[0].message.content.strip()
        return html_content
    except Exception as e:
        print(f"[GPT] Erreur génération HTML : {e}")
        return "<p>Erreur lors de la génération de la lettre.</p>"
