import requests
from bs4 import BeautifulSoup

def scrape_all_with_email():
    """Scrape plusieurs sites d'offres en lien avec l'IA et retourne uniquement celles avec email."""
    jobs = []

    # Exemple 1: WeWorkRemotely
    try:
        url = "https://weworkremotely.com/categories/remote-ai-jobs"
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "html.parser")
        for job_section in soup.select("section.jobs article"):
            title_elem = job_section.select_one("span.title")
            company_elem = job_section.select_one("span.company")
            apply_link = job_section.select_one("a")
            email = job_section.get("data-email")  # exemple, dépend du site
            if title_elem and email:
                jobs.append({
                    "title": title_elem.text.strip(),
                    "company": company_elem.text.strip() if company_elem else "",
                    "apply_email": email.strip(),
                    "source": "WeWorkRemotely",
                    "url": apply_link['href'] if apply_link else ""
                })
    except Exception as e:
        print(f"[WeWorkRemotely] Erreur lors du scraping : {e}")

    # Ajouter d'autres sites similaires ici (RemoteOK, Indeed, etc.)

    return jobs
