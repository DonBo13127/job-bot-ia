import requests
from bs4 import BeautifulSoup

def scrape_all():
    jobs = []

    # Exemple simple WeWorkRemotely
    url = "https://weworkremotely.com/remote-jobs/search?term=AI"
    try:
        res = requests.get(url)
        soup = BeautifulSoup(res.text, "html.parser")
        offers = soup.select("section.jobs article")
        for offer in offers:
            title_tag = offer.select_one("span.title")
            company_tag = offer.select_one("span.company")
            link_tag = offer.select_one("a")
            if title_tag and company_tag and link_tag:
                title = title_tag.text.strip()
                company = company_tag.text.strip()
                link = "https://weworkremotely.com" + link_tag["href"]
                # Filtrage IA
                keywords = ["AI", "Machine Learning", "Deep Learning", "Artificial Intelligence"]
                if any(k.lower() in title.lower() for k in keywords):
                    jobs.append({
                        "title": title,
                        "company": company,
                        "url": link,
                        "source": "WeWorkRemotely",
                        "apply_email": None  # pas d'email direct
                    })
    except Exception as e:
        print(f"[WeWorkRemotely] Erreur lors du scraping: {e}")

    return jobs
