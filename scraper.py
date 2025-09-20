import re
import requests
from bs4 import BeautifulSoup

def scrape_all_with_email():
    """
    Scrape uniquement les offres IA avec email.
    Retourne une liste de dictionnaires :
    [{'title': ..., 'company': ..., 'email': ..., 'url': ...}, ...]
    """
    offers = []
    urls = [
        "https://weworkremotely.com/categories/remote-ai-jobs",
        "https://remoteok.com/remote-ai-jobs"
    ]

    email_regex = re.compile(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+')

    for url in urls:
        resp = requests.get(url)
        if resp.status_code != 200:
            continue
        soup = BeautifulSoup(resp.text, "html.parser")
        for job in soup.find_all("a", href=True):
            text = job.get_text()
            link = job['href']
            emails = email_regex.findall(text)
            if emails:
                offers.append({
                    "title": text.strip(),
                    "company": "",  # ajouter extraction si disponible
                    "email": emails[0],
                    "url": link
                })
    return offers
