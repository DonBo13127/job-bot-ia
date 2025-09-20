import requests
from bs4 import BeautifulSoup
import re

def scrape_ai_with_email():
    jobs = []

    # Sites scrappables publics
    sites = [
        {
            "name": "WeWorkRemotely",
            "url": "https://weworkremotely.com/categories/remote-remote-jobs",
            "job_selector": "section.jobs article",
            "title_selector": "span.title",
            "company_selector": "span.company",
            "link_selector": "a"
        },
        {
            "name": "WTTJ",
            "url": "https://www.welcometothejungle.com/en/jobs?query=AI",
            "job_selector": "li.sc-eCstlR",
            "title_selector": "h3",
            "company_selector": "p",
            "link_selector": "a"
        }
        # Ajouter d'autres sites si nécessaire
    ]

    for site in sites:
        try:
            resp = requests.get(site["url"])
            if resp.status_code != 200:
                print(f"[{site['name']}] Erreur HTTP {resp.status_code}")
                continue

            soup = BeautifulSoup(resp.text, "html.parser")
            job_cards = soup.select(site["job_selector"])

            for card in job_cards:
                title_el = card.select_one(site["title_selector"])
                company_el = card.select_one(site["company_selector"])
                link_el = card.select_one(site["link_selector"])

                if not title_el or not link_el:
                    continue

                job_url = link_el.get("href")
                if not job_url.startswith("http"):
                    job_url = site["url"].split("/jobs")[0] + job_url

                try:
                    job_page = requests.get(job_url)
                    emails = re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", job_page.text)
                    if not emails:
                        continue
                except:
                    continue

                jobs.append({
                    "title": title_el.get_text(strip=True),
                    "company": company_el.get_text(strip=True) if company_el else "Inconnue",
                    "url": job_url,
                    "source": site["name"],
                    "apply_email": emails[0]
                })

        except Exception as e:
            print(f"[{site['name']}] Erreur : {e}")

    print(f"✅ {len(jobs)} annonces IA avec email trouvées.")
    return jobs
