# scraper.py
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time


# -----------------------------
# 1. Welcome to the Jungle (FR) - https://wttj.fr
# -----------------------------
def scrape_wttj():
    """Scrape les offres sur welcome to the jungle (FR)"""
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
            company_elem = job.select_one('span[data-testid="job-card-company-name"]')
            location_elem = job.select_one('li span + span')

            title = title_elem.get_text(strip=True) if title_elem else "N/A"
            company = company_elem.get_text(strip=True) if company_elem else "N/A"
            location = location_elem.get_text(strip=True).lower() if location_elem else ""
            link = urljoin("https://www.welcometothejungle.com", job['href'])

            keywords = ['scrap', 'auto', 'ia', 'bot', 'agent', 'intelligence artificielle', 'automatisation', 'rpa', 'llm']
            text_lower = f"{title} {company}".lower()

            if any(kw in text_lower for kw in keywords) and ("remote" in location or "télétravail" in location):
                jobs.append({
                    "title": title,
                    "company": company,
                    "url": link,
                    "location": "Remote",
                    "language": "fr",
                    "site": "wttj"
                })
    except Exception as e:
        print(f"[WTTJ] Erreur : {e}")
    return jobs


# -----------------------------
# 2. Meteors AI (Global) - https://www.meteors.ai
# -----------------------------
def scrape_meteors():
    """Scrape meteors.ai - Agents IA & Automatisation"""
    url = "https://www.meteors.ai/jobs"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"
    }
    jobs = []
    try:
        r = requests.get(url, headers=headers, timeout=10)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, 'html.parser')

        for job in soup.select('.job-card'):
            title_elem = job.select_one('h3 a')
            company_elem = job.select_one('.company-name')

            title = title_elem.get_text(strip=True) if title_elem else "N/A"
            company = company_elem.get_text(strip=True) if company_elem else "N/A"
            link = urljoin("https://www.meteors.ai", title_elem['href']) if title_elem and title_elem.get('href') else None

            if not link:
                continue

            if any(kw in f"{title} {company}".lower() for kw in ['scrap', 'auto', 'ia', 'agent', 'ai', 'automation', 'bot']):
                language = "en"
                if any(c in 'áéíóúñ¡¿' for c in title): language = "es"
                elif any(c in 'àâäéêèûù' for c in title): language = "fr"

                jobs.append({
                    "title": title,
                    "company": company,
                    "url": link,
                    "location": "Remote",
                    "language": language,
                    "site": "meteors"
                })
    except Exception as e:
        print(f"[Meteors] Erreur : {e}")
    return jobs


# -----------------------------
# 3. Remotive (Global) - https://remotive.io
# -----------------------------
def scrape_remotive():
    """Scrape remotive.io - Catégorie Intelligence Artificielle"""
    url = "https://remotive.io/remote-jobs?category=artificial-intelligence"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"
    }
    jobs = []
    try:
        r = requests.get(url, headers=headers, timeout=10)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, 'html.parser')

        for job in soup.select('.job'):
            title_elem = job.select_one('h3')
            company_elem = job.select_one('.company_name')
            detail_url = job.select_one('a')['href'] if job.select_one('a') else None

            title = title_elem.get_text(strip=True) if title_elem else "N/A"
            company = company_elem.get_text(strip=True) if company_elem else "N/A"
            link = urljoin("https://remotive.io", detail_url) if detail_url else None

            if not link:
                continue

            if any(kw in title.lower() for kw in ['scrap', 'auto', 'ia', 'agent', 'ai', 'automation', 'bot', 'crawler']):
                jobs.append({
                    "title": title,
                    "company": company,
                    "url": link,
                    "location": "Remote",
                    "language": "en",
                    "site": "remotive"
                })
    except Exception as e:
        print(f"[Remotive] Erreur : {e}")
    return jobs


# -----------------------------
# 4. YesWeRemote (FR) - https://yesweremote.fr
# -----------------------------
def scrape_yesweremote():
    """Scrape yesweremote.fr - Startups françaises en remote"""
    url = "https://yesweremote.fr/jobs?search=ia+automatisation"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"
    }
    jobs = []
    try:
        r = requests.get(url, headers=headers, timeout=10)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, 'html.parser')

        for job in soup.select('a[href^="/jobs/"]'):
            title_elem = job.select_one('h2')
            company_elem = job.select_one('.text-gray-600')

            title = title_elem.get_text(strip=True) if title_elem else "N/A"
            company = company_elem.get_text(strip=True) if company_elem else "N/A"
            link = urljoin("https://yesweremote.fr", job['href'])

            if any(kw in title.lower() for kw in ['scrap', 'auto', 'ia', 'agent', 'automation']):
                jobs.append({
                    "title": title,
                    "company": company,
                    "url": link,
                    "location": "Remote",
                    "language": "fr",
                    "site": "yesweremote"
                })
    except Exception as e:
        print(f"[YesWeRemote] Erreur : {e}")
    return jobs


# -----------------------------
# Fonction principale : exécute tous les scrapers
# -----------------------------
def scrape_all():
    """
    Lance tous les scrapers et retourne une liste unique d'offres.
    Ajoute un délai entre chaque site pour éviter les blocages.
    """
    all_jobs = []
    scrapers = [
        ("Welcome to the Jungle", scrape_wttj),
        ("Meteors AI", scrape_meteors),
        ("Remotive", scrape_remotive),
        ("YesWeRemote", scrape_yesweremote)
    ]

    for name, scraper in scrapers:
        print(f"[{name}] Scraping en cours...")
        try:
            jobs = scraper()
            print(f"[{name}] ✅ {len(jobs)} offre(s) trouvée(s).")
            all_jobs.extend(jobs)
        except Exception as e:
            print(f"[{name}] ❌ Échec: {e}")
        time.sleep(3)  # Respectons les serveurs

    print(f"\n[Total] 🎯 {len(all_jobs)} offre(s) collectée(s).")
    return all_jobs
