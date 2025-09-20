import requests
from bs4 import BeautifulSoup
import re

# Liste de sites scrappables
SITES = [
    {"url": "https://weworkremotely.com/categories/remote-ai-jobs", "source": "WeWorkRemotely"},
    {"url": "https://remoteok.com/remote-ai-jobs", "source": "RemoteOK"},
    # Ajouter d'autres sites IA scrappables
]

EMAIL_REGEX = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"

def scrape_ai_jobs_with_email():
    jobs = []
    for site in SITES:
        try:
            r = requests.get(site["url"], headers={"User-Agent": "Mozilla/5.0"})
            soup = BeautifulSoup(r.text, "html.parser")
            # Exemples simples de parsing, à adapter selon structure des sites
            for job_card in soup.find_all("a", href=True):
                title = job_card.get_text(strip=True)
                link = job_card["href"]
                if "ai" in title.lower():  # filtrage IA
                    text = job_card.get_text(" ", strip=True)
                    emails = re.findall(EMAIL_REGEX, text)
                    if emails:
                        job = {
                            "title": title,
                            "company": "Non précisé",
                            "apply_email": emails[0],
                            "source": site["source"],
                            "link": link,
                            "lang": "fr" if any(c in title for c in "éèà") else "es"
                        }
                        jobs.append(job)
        except Exception as e:
            print(f"[{site['source']}] Erreur scraping : {e}")
    return jobs
