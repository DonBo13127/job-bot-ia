import requests

def scrape_wttj():
    url = "https://www.welcometothejungle.com/fr/jobs?ref=api"
    try:
        r = requests.get(url)
        jobs = r.json().get("jobs", [])
        results = []
        for job in jobs:
            results.append({
                "title": job.get("title"),
                "company": job.get("company_name"),
                "url": job.get("seo_url"),
                "source": "WTTJ",
                "apply_email": job.get("apply_email")  # si dispo
            })
        return results
    except:
        print("[WTTJ] Erreur lors du scraping")
        return []

def scrape_remotive():
    url = "https://remotive.io/api/remote-jobs?category=software-dev"
    try:
        r = requests.get(url)
        jobs = r.json().get("jobs", [])
        results = []
        for job in jobs:
            results.append({
                "title": job.get("title"),
                "company": job.get("company_name"),
                "url": job.get("url"),
                "source": "Remotive",
                "apply_email": job.get("apply_email")
            })
        return results
    except:
        print("[Remotive] Erreur lors du scraping")
        return []

def scrape_weworkremotely():
    url = "https://weworkremotely.com/categories/remote-programming-jobs.rss"
    try:
        r = requests.get(url)
        # parsing RSS simple (titre + lien)
        results = []
        import xml.etree.ElementTree as ET
        root = ET.fromstring(r.content)
        for item in root.findall(".//item"):
            results.append({
                "title": item.find("title").text,
                "company": item.find("author").text if item.find("author") is not None else "",
                "url": item.find("link").text,
                "source": "WeWorkRemotely",
                "apply_email": None
            })
        return results
    except:
        print("[WeWorkRemotely] Erreur lors du scraping")
        return []

def scrape_all():
    jobs = []
    jobs += scrape_wttj()
    jobs += scrape_remotive()
    jobs += scrape_weworkremotely()
    print(f"✅ {len(jobs)} offres collectées.")
    return jobs
