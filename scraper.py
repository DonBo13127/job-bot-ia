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
    url = "https://www.welcometothejungle.com/fr/jobs?k=automation&l=France&r=true"
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
            company_elem = job.select_one('[data-testid="job-card-company-name"]')

            title = title_elem.get_text(strip=True) if title_elem else "N/A"
            company = company_elem.get_text(strip=True) if company_elem else "N/A"
            link = urljoin("https://www.welcometothejungle.com", job['href'])

            keywords = ['scrap', 'auto', 'ia', 'agent', 'intelligence artificielle', 'automatisation', 'rpa', 'bot']
            if any(kw in title.lower() for kw in keywords):
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
# 2. Remotive (Global) - https://remotive.io
# -----------------------------
def scrape_remotive():
    """Scrape remotive.io - Catégorie Intelligence Artificielle"""
    url = "https://remotive.io/remote-jobs/ai-machine-learning"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"
    }
    jobs = []
    try:
        r = requests.get(url, headers=headers, timeout=10)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, 'html.parser')

        for job in soup.select('.job_listings .job'):
            title_elem = job.select_one('h3 a')
            company_elem = job.select_one('.company a')
            detail_url = job.select_one('a')['href'] if job.select_one('a') else None

            title = title_elem.get_text(strip=True) if title_elem else "N/A"
            company = company_elem.get_text(strip=True) if company_elem else "N/A"
            link = urljoin("https://remotive.io", detail_url) if detail_url else None

            if not link:
                continue

            if any(kw in title.lower() for kw in ['scrap', 'auto', 'ia', 'agent', 'ai', 'automation', 'bot']):
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
# 3. Turing (Global) - https://turing.com
# -----------------------------
def scrape_turing():
    """Scrape turing.com - Jobs IA / Automatisation / Full Remote"""
    url = "https://turing.com/jobs"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"
    }
    jobs = []
    try:
        r = requests.get(url, headers=headers, timeout=10)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, 'html.parser')

        for job in soup.select('a[href^="/jobs/"]'):
            title_elem = job.select_one('h3')
            company_elem = job.select_one('.company')
            location_elem = job.select_one('.location')

            if not title_elem or not company_elem:
                continue

            title = title_elem.get_text(strip=True)
            company = company_elem.get_text(strip=True)
            link = urljoin("https://turing.com", job['href'])

            # Vérifier que c'est bien remote
            is_remote = location_elem and 'worldwide' in location_elem.get_text().lower()

            keywords = ['ai', 'agent', 'automation', 'bot', 'scrap', 'ml', 'intelligence']
            if any(kw in title.lower() for kw in keywords) and is_remote:
                jobs.append({
                    "title": title,
                    "company": company,
                    "url": link,
                    "location": "Remote",
                    "language": "en",
                    "site": "turing"
                })
    except Exception as e:
        print(f"[Turing] Erreur : {e}")
    return jobs


# -----------------------------
# 4. EuropeRemoto (FR/ES) - https://europoremoto.com
# -----------------------------
def scrape_europoremoto():
    """Scrape europoremoto.com - Offres FR/ES en remote"""
    url = "https://europoremoto.com/jobs?search=ia+automation"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"
    }
    jobs = []
    try:
        r = requests.get(url, headers=headers, timeout=10)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, 'html.parser')

        for job in soup.select('a.block[href^="/jobs/detail"]'):
            title_elem = job.select_one('h2')
            company_elem = job.select_one('p.text-gray-600')

            if not title_elem or not company_elem:
                continue

            title = title_elem.get_text(strip=True)
            company = company_elem.get_text(strip=True)
            link = urljoin("https://europoremoto.com", job['href'])

            if any(kw in title.lower() for kw in ['ia', 'ai', 'auto', 'scrap', 'agent']):
                language = "es" if any(c in title for c in 'ñáéíóú¿¡') else "fr"

                jobs.append({
                    "title": title,
                    "company": company,
                    "url": link,
                    "location": "Remote",
                    "language": language,
                    "site": "europoremoto"
                })
    except Exception as e:
        print(f"[Europoremoto] Erreur : {e}")
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
        ("Remotive", scrape_remotive),
        ("Turing", scrape_turing),
        ("EuropeRemoto", scrape_europoremoto)
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
