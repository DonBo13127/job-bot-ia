# scraper.py
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time


# -----------------------------
# Scraper 1 : Welcome to the Jungle (FR) - Full Remote + Tech IA
# -----------------------------
def scrape_wttj():
    """
    Scraping des offres sur Welcome to the Jungle
    Recherche : automation, IA, scraping, agent IA, etc.
    """
    url = "https://www.welcometothejungle.com/fr/jobs?query=ia%20automation%20scraping&refinementList%5Bremote%5D%5B%5D=remote"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"
    }
    jobs = []
    try:
        r = requests.get(url, headers=headers, timeout=10)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, 'html.parser')

        for job in soup.select('a[data-testid="job-card"]'):
            title_elem = job.select_one('h2')
            company_elem = job.select_one('span.sc-gyigFi')  # ou autre classe dynamique
            location_elem = job.select_one('li span + span')  # localisation

            title = title_elem.get_text(strip=True) if title_elem else "N/A"
            company = company_elem.get_text(strip=True) if company_elem else "N/A"
            location = location_elem.get_text(strip=True) if location_elem else ""
            link = urljoin("https://www.welcometothejungle.com", job['href'])

            # Mots-clés pertinents
            keywords = ['scrap', 'auto', 'ia', 'bot', 'agent', 'intelligence artificielle', 'automatisation', 'rpa', 'llm']
            text_lower = (title + ' ' + company).lower()

            if any(kw in text_lower for kw in keywords):
                if "remote" in text_lower or "télétravail" in text_lower or "worldwide" in location.lower():
                    jobs.append({
                        "title": title,
                        "company": company,
                        "url": link,
                        "location": "Remote",
                        "language": "fr",
                        "site": "wttj"
                    })
    except Exception as e:
        print(f"[WTTJ] Erreur de scraping : {e}")
    return jobs


# -----------------------------
# Scraper 2 : Meteors.dev (Dev IA / Agents / Remote)
# -----------------------------
def scrape_meteors():
    """
    Meteors.dev : Offres tech IA, souvent en anglais mais cibles francophones
    """
    url = "https://meteors.dev/jobs"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"
    }
    jobs = []
    try:
        r = requests.get(url, headers=headers, timeout=10)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, 'html.parser')

        for job in soup.select('.job-listing'):
            title_elem = job.select_one('h3 a')
            company_elem = job.select_one('.company-name')
            tag_elems = [t.get_text(strip=True).lower() for t in job.select('.tag')]
            remote = any('remote' in t for t in tag_elems)

            title = title_elem.get_text(strip=True) if title_elem else "N/A"
            company = company_elem.get_text(strip=True) if company_elem else "N/A"
            link = urljoin("https://meteors.dev", title_elem['href']) if title_elem and title_elem.get('href') else None

            if not link:
                continue

            keywords = ['scrap', 'auto', 'ia', 'agent', 'ai', 'automation', 'bot', 'crawler', 'llm']
            if any(kw in (title + ' ' + ' '.join(tag_elems)).lower() for kw in keywords) and remote:
                language = "en"
                if any(c in title for c in ['á', 'é', 'ñ', 'ó', 'ú', '¡', '¿']):  # Espagnol approximatif
                    language = "es"
                elif any(c in ['é', 'à', 'ù', 'ê', 'î'] for c in title):
                    language = "fr"

                jobs.append({
                    "title": title,
                    "company": company,
                    "url": link,
                    "location": "Remote",
                    "language": language,
                    "site": "meteors"
                })
    except Exception as e:
        print(f"[Meteors] Erreur de scraping : {e}")
    return jobs


# -----------------------------
# Scraper 3 : Remotive.io (Remote jobs)
# -----------------------------
def scrape_remotive():
    """
    Remotive : Catégorie "AI / Machine Learning"
    """
    url = "https://remotive.io/remote-jobs/ai-machine-learning"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"
    }
    jobs = []
    try:
        r = requests.get(url, headers=headers, timeout=10)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, 'html.parser')

        for job in soup.select('.job-tile'):
            title_elem = job.select_one('.position')
            company_elem = job.select_one('.company')
            detail_url = job.select_one('a')['href']

            title = title_elem.get_text(strip=True) if title_elem else "N/A"
            company = company_elem.get_text(strip=True) if company_elem else "N/A"
            link = urljoin("https://remotive.io", detail_url)

            keywords = ['scrap', 'auto', 'ia', 'agent', 'ai', 'automation', 'bot', 'data extraction']
            if any(kw in title.lower() for kw in keywords):
                jobs.append({
                    "title": title,
                    "company": company,
                    "url": link,
                    "location": "Remote",
                    "language": "en",
                    "site": "remotive"
                })
    except Exception as e:
        print(f"[Remotive] Erreur de scraping : {e}")
    return jobs


# -----------------------------
# Scraper 4 : YesWeRemote (France & Europe Remote)
# -----------------------------
def scrape_yesweremote():
    """
    YesWeRemote : Startups françaises en remote
    """
    url = "https://yesweremote.com/jobs?search=ai+automation"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"
    }
    jobs = []
    try:
        r = requests.get(url, headers=headers, timeout=10)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, 'html.parser')

        for job in soup.select('a[href^="/jobs/detail"]'):
            title_elem = job.select_one('h2')
            company_elem = job.select_one('div.flex-grow p')
            location_elem = job.select_one('div.flex-shrink p')

            title = title_elem.get_text(strip=True) if title_elem else "N/A"
            company = company_elem.get_text(strip=True) if company_elem else "N/A"
            location = location_elem.get_text(strip=True) if location_elem else ""

            if "remote" not in location.lower():
                continue

            link = urljoin("https://yesweremote.com", job['href'])

            keywords = ['scrap', 'auto', 'ia', 'agent', 'bot', 'automation', 'crawler']
            if any(kw in title.lower() for kw in keywords):
                jobs.append({
                    "title": title,
                    "company": company,
                    "url": link,
                    "location": "Remote",
                    "language": "fr",
                    "site": "yesweremote"
                })
    except Exception as e:
        print(f"[YesWeRemote] Erreur de scraping : {e}")
    return jobs


# -----------------------------
# Fonction principale : exécute tous les scrapers
# -----------------------------
def scrape_all():
    """
    Lance tous les scrapers et retourne une liste unique d'offres
    """
    all_jobs = []
    scrapers = [
        ("Welcome to the Jungle", scrape_wttj),
        ("Meteors", scrape_meteors),
        ("Remotive", scrape_remotive),
        ("YesWeRemote", scrape_yesweremote)
    ]

    for name, scraper in scrapers:
        print(f"[{name}] Scraping en cours...")
        jobs = scraper()
        print(f"[{name}] {len(jobs)} offres trouvées.")
        all_jobs.extend(jobs)
        time.sleep(2)  # Respectons les serveurs

    print(f"[Total] {len(all_jobs)} offres collectées.")
    return all_jobs
