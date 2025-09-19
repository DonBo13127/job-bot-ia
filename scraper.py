# scraper.py
import requests
from bs4 import BeautifulSoup
import time
from urllib.parse import urljoin

def scrape_wttj():
    """Scraper Welcome to the Jungle (FR)"""
    url = "https://www.welcometothejungle.com/fr/jobs?refinementList%5Bremote%5D%5B%5D=remote&query=automation%20IA%20scraping"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    jobs = []
    try:
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.text, 'html.parser')
        for job in soup.select('a.sc-eqIVtm'):  # Sélecteur typique
            title = job.select_one('h2')?.get_text(strip=True) or "N/A"
            company = job.select_one('span.sc-gyigGi')?.get_text(strip=True) or "N/A"
            link = urljoin("https://wttj.fr", job['href'])
            location = "Remote"
            if "remote" in link.lower() and ("scrap" in title.lower() or "auto" in title.lower() or "ia" in title.lower()):
                jobs.append({
                    "title": title,
                    "company": company,
                    "url": link,
                    "location": location,
                    "language": "fr",
                    "site": "wttj"
                })
    except Exception as e:
        print(f"[WTTJ] Erreur: {e}")
    return jobs
