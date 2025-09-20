def generate_cover_letter(job, language="fr"):
    prompt_fr = f"""
    Tu es un expert RH et rédiges des lettres de motivation très convaincantes.
    Rédige une lettre courte et professionnelle pour ce poste :
    - Titre : {job.get('title')}
    - Entreprise : {job.get('company')}
    - Lien de l'offre : {job.get('url')}
    
    Le candidat :
    - S'appelle Yacine BEDHOUCHE
    - Testeur certifié ISTQB avec 3 ans d'expérience
    - Expert en automatisation avec Robot Framework
    - Spécialiste en Intelligence Artificielle appliquée à la QA
    - Capable de gérer des projets QA complexes, d'optimiser les processus et d'améliorer la qualité logicielle

    La lettre doit :
    - Montrer sa motivation
    - Mettre en avant ses compétences en QA, automatisation et IA
    - Être concise, professionnelle et convaincante
    - Inclure une référence visuelle : "Je m'imagine dans un environnement IT moderne, comme sur cette image : https://www.freepik.com/photos-gratuite/specialiste-informatique-dans-ferme-serveurs-minimisant-defaillances-machines_264385749.htm#fromView=search&page=1&position=5&uuid=f6600eb9-89a4-4b30-94a2-d917bd260646&query=IT"
    """

    prompt_es = f"""
    Eres un experto en recursos humanos y redactas cartas de motivación muy convincentes.
    Redacta una carta breve y profesional para este puesto:
    - Puesto: {job.get('title')}
    - Empresa: {job.get('company')}
    - Enlace de la oferta: {job.get('url')}
    
    El candidato:
    - Se llama Yacine BEDHOUCHE
    - Tester certificado ISTQB con 3 años de experiencia
    - Experto en automatización con Robot Framework
    - Especialista en Inteligencia Artificial aplicada a QA
    - Capaz de gestionar proyectos QA complejos, optimizar procesos y mejorar la calidad del software

    La carta debe:
    - Mostrar motivación
    - Resaltar sus habilidades en QA, automatización e IA
    - Ser concisa, profesional y convincente
    - Incluir una referencia visual: "Me imagino en un entorno IT moderno, como en esta imagen: https://www.freepik.com/photos-gratuite/specialiste-informatique-dans-ferme-serveurs-minimisant-defaillances-machines_264385749.htm#fromView=search&page=1&position=5&uuid=f6600eb9-89a4-4b30-94a2-d917bd260646&query=IT"
    """

    prompt = prompt_fr if language == "fr" else prompt_es

    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Tu es un assistant RH expert."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=400
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"[GPT] Erreur : {e}")
        return ""
