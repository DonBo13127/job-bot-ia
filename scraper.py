import requests

def scrape_all_ai():
    """
    Scrape des offres liées à l'IA depuis plusieurs sources.
    Retourne une liste de dicts avec : title, company, url, apply_email, source
    """
    jobs = []

    # Exemple WeWorkRemotely
    try:
        resp = requests.get("https://weworkremotely.com/categories/remote-ai-jobs")
        if resp.status_code == 200:
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(resp.text, "html.parser")
            listings = soup.select("section.jobs article li a")
            for link in listings:
                title = link.find("span", class_="title").text if link.find("span", class_="title") else "Sans titre"
                company = link.find("span", class_="company").text if link.find("span", class_="company") else "Inconnue"
                url = "https://weworkremotely.com" + link.get("href")
                jobs.append({
                    "title": title,
                    "company": company,
                    "url": url,
                    "apply_email": None,  # On pourra extraire plus tard si disponible
                    "source": "WeWorkRemotely"
                })
    except Exception as e:
        print(f"[WeWorkRemotely] Erreur lors du scraping : {e}")

    # Exemple Remotive.io
    try:
        resp = requests.get("https://remotive.io/api/remote-jobs?search=AI")
        if resp.status_code == 200:
            data = resp.json()
            for job in data.get("jobs", []):
                jobs.append({
                    "title": job.get("title"),
                    "company": job.get("company_name"),
                    "url": job.get("url"),
                    "apply_email": None,  # à compléter si disponible
                    "source": "Remotive"
                })
    except Exception as e:
        print(f"[Remotive] Erreur lors du scraping : {e}")

    # On peut ajouter d'autres sources ici

    return jobs
