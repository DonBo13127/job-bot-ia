import re

def scrape_all_ai_with_email():
    """
    Exemple : renvoie une liste d'offres IA avec email.
    Chaque job = dict(title, company, link, apply_email, source, lang)
    """
    # Exemple statique, à remplacer par ton scraper réel
    jobs = [
        {
            "title": "AI Engineer",
            "company": "Vidrush",
            "link": "https://weworkremotely.com/...",
            "apply_email": "hr@vidrush.com",
            "source": "WeWorkRemotely",
            "lang": "en"
        },
        {
            "title": "Ingeniero IA",
            "company": "TechSol",
            "link": "https://trabajoremoto.com/...",
            "apply_email": "contact@techsol.com",
            "source": "TrabajoRemoto",
            "lang": "es"
        }
    ]

    # Filtre seulement les emails
    return [job for job in jobs if job.get("apply_email")]
