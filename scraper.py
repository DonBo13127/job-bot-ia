import requests
from bs4 import BeautifulSoup
import re

def scrape_ai_with_email():
    jobs = []

    # Exemple WeWorkRemotely
    url = "https://weworkremotely.com/categories/remote-remote-jobs"
    try:
        resp = requests.get(url)
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.text, "html.parser")
            # boucle simplifiée d'exemple
            job_cards = soup.select("section.jobs article")
            for card in job_cards:
                title = card.select_one("span.title")
                company = card.select_one("span.company")
                link = card.find("a", href=True)

                if not title or not link or not company:
                    continue

                # Simuler extraction email (dans la vraie version on parse l'offre complète)
                job_page = requests.get("https://weworkremotely.com" + link['href'])
                emails = re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", job_page.text)

                if emails:
                    jobs.append({
                        "title": title.get_text(strip=True),
                        "company": company.get_text(strip=True),
                        "url": "https://weworkremotely.com" + link['href'],
                        "source": "WeWorkRemotely",
                        "apply_email": emails[0]  # prend le premier email trouvé
                    })
    except Exception as e:
        print(f"[WeWorkRemotely] Erreur lors du scraping : {e}")

    return jobs
