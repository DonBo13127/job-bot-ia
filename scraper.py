import requests

def scrape_all_ai():
    jobs = []

    # Exemple WeWorkRemotely
    url = "https://weworkremotely.com/categories/remote-remote-jobs"
    try:
        resp = requests.get(url)
        if resp.status_code == 200:
            # Ici tu ajoutes ton parsing HTML/JSON
            # Filtrer uniquement les jobs IA
            jobs.append({
                "title": "AI Engineer",
                "company": "Vidrush",
                "url": "https://weworkremotely.com/remote-jobs/ai-engineer",
                "source": "WeWorkRemotely",
                "apply_email": "hr@vidrush.com"
            })
    except Exception as e:
        print(f"[WeWorkRemotely] Erreur lors du scraping : {e}")

    return jobs
