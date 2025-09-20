import requests
import feedparser

# =============================
#  Welcome to the Jungle (WTTJ)
# =============================
def scrape_wttj(query="python"):
    url = f"https://www.welcometothejungle.com/api/v1/jobs?query={query}&language=fr&limit=10&page=1"
    try:
        resp = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        resp.raise_for_status()
        jobs = resp.json().get("jobs", [])
        results = []
        for job in jobs:
            results.append({
                "source": "Welcome to the Jungle",
                "title": job["name"],
                "company": job["company"]["name"],
                "url": f"https://www.welcometothejungle.com/fr/companies/{job['company']['slug']}/jobs/{job['slug']}"
            })
        return results
    except Exception as e:
        print(f"[WTTJ] Erreur : {e}")
        return []


# =============================
#  Remotive (API officielle)
# =============================
def scrape_remotive(category="software-dev"):
    url = f"https://remotive.io/api/remote-jobs?category={category}"
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        jobs = resp.json().get("jobs", [])
        results = []
        for job in jobs:
            results.append({
                "source": "Remotive",
                "title": job["title"],
                "company": job["company_name"],
                "url": job["url"],
                "location": job["candidate_required_location"]
            })
        return results
    except Exception as e:
        print(f"[Remotive] Erreur : {e}")
        return []


# =============================
#  WeWorkRemotely (RSS feed)
# =============================
def scrape_weworkremotely():
    url = "https://weworkremotely.com/categories/remote-programming-jobs.rss"
    try:
        feed = feedparser.parse(url)
        results = []
        for entry in feed.entries:
            results.append({
                "source": "WeWorkRemotely",
                "title": entry.title,
                "company": entry.title.split(":")[0],
                "url": entry.link
            })
        return results
    except Exception as e:
        print(f"[WeWorkRemotely] Erreur : {e}")
        return []


# =============================
#  RemoteOK (API officielle)
# =============================
def scrape_remoteok():
    url = "https://remoteok.com/api"
    try:
        resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        resp.raise_for_status()
        jobs = resp.json()[1:]  # le premier élément est une bannière
        results = []
        for job in jobs:
            results.append({
                "source": "RemoteOK",
                "title": job.get("position"),
                "company": job.get("company"),
                "url": job.get("url")
            })
        return results
    except Exception as e:
        print(f"[RemoteOK] Erreur : {e}")
        return []


# =============================
#  Fonction principale
# =============================
def scrape_all():
    all_jobs = []
    all_jobs.extend(scrape_wttj("python"))
    all_jobs.extend(scrape_remotive("software-dev"))
    all_jobs.extend(scrape_weworkremotely())
    all_jobs.extend(scrape_remoteok())
    return all_jobs


if __name__ == "__main__":
    print("🔍 Collecte des offres d'emploi...")
    jobs = scrape_all()
    print(f"[Total] 🎯 {len(jobs)} offre(s) collectée(s).")
    for job in jobs[:10]:  # affiche seulement les 10 premières
        print(f"- {job['source']} | {job['title']} @ {job.get('company', 'N/A')} -> {job['url']}")
