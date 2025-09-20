import requests
from bs4 import BeautifulSoup
import re
import time

# Sites scrappables IA
SITES = [
    {"url": "https://weworkremotely.com/categories/remote-ai-jobs", "source": "WeWorkRemotely"},
    {"url": "https://remoteok.com/remote-ai-jobs", "source": "RemoteOK"},
    # Ajouter d'autres sites IA scrappables
]

EMAIL_REGEX = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

def fetch_page(url, retries=3):
    """Récupère une page avec gestion des erreurs et retries."""
    for i in range(retries):
        try:
            r = requests.get(url, headers=HEADERS, timeout=15)
            r.raise_for_status()
            return r.text
        except Exception as e:
            print(f"⚠️ Erreur fetch {url} ({i+1}/{retries}) : {e}")
            time.sleep(2)
    return None

def extract_email_from_text(text):
    emails = re.findall(EMAIL_REGEX, text)
    return emails[0] if emails else None

def scrape_ai_jobs_with_email():
    jobs = []

    for site in SITES:
        print(f"🔍 Scraping {site['source']} ...")
        html = fetch_page(site["url"])
        if not html:
            continue

        soup = BeautifulSoup(html, "html.parser")

        # Parcours générique des liens
        for link_tag in soup.find_all("a", href=True):
            title = link_tag.get_text(strip=True)
            href = link_tag["href"]
            if "ai" not in title.lower():
                continue  # filtrage IA

            # Récupération page détail pour email
            detail_url = href if href.startswith("http") else site["url"].split("/categories")[0] + href
            detail_html = fetch_page(detail_url)
            if not detail_html:
                continue

            email = extract_email_from_text(detail_html)
            if not email:
                continue  # ignore si pas d'email

            lang = "fr" if any(c in title for c in "éèàç") else "es"

            job = {
                "title": title,
                "company": "Non précisé",
                "apply_email": email,
                "source": site["source"],
                "link": detail_url,
                "lang": lang
            }
            jobs.append(job)

    print(f"✅ {len(jobs)} offres IA avec email trouvées.")
    return jobs
