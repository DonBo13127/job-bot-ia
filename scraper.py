import re
import requests
from bs4 import BeautifulSoup

AI_KEYWORDS = ['artificial intelligence', 'machine learning', 'deep learning', 'IA', 'inteligencia artificial']

def scrape_ai_jobs():
    """
    Scrape les offres IA sur des sites publics et retourne une liste de jobs avec email.
    """
    offers = []
    urls = [
        "https://weworkremotely.com/categories/remote-ai-jobs",
        "https://remoteok.com/remote-ai-jobs"
    ]
    email_regex = re.compile(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+')

    for url in urls:
        try:
            resp = requests.get(url, timeout=10)
            if resp.status_code != 200:
                continue
            soup = BeautifulSoup(resp.text, "html.parser")
            for job in soup.find_all("a", href=True):
                text = job.get_text().lower()
                link = job['href']
                if any(keyword.lower() in text for keyword in AI_KEYWORDS):
                    emails = email_regex.findall(text)
                    if emails:
                        offers.append({
                            "title": job.get_text().strip(),
                            "company": "",
                            "email": emails[0],
                            "url": link
                        })
        except Exception:
            continue
    return offers
