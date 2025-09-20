import requests
from bs4 import BeautifulSoup

def scrape_all_with_email():
    jobs = []

    # Exemple: WeWorkRemotely AI jobs
    url = "https://weworkremotely.com/categories/remote-ai-jobs"
    try:
        resp = requests.get(url)
        soup = BeautifulSoup(resp.text, "html.parser")
        for li in soup.select("section.jobs > article > ul > li"):
            a_tag = li.find("a", href=True)
            if not a_tag:
                continue
            title = a_tag.text.strip()
            job_url = "https://weworkremotely.com" + a_tag['href']
            # Extraction email simple : placeholder
            apply_email = extract_email_from_job(job_url)
            if apply_email:
                jobs.append({
                    "title": title,
                    "company": "WeWorkRemotely",
                    "source": "WeWorkRemotely",
                    "url": job_url,
                    "apply_email": apply_email
                })
    except Exception as e:
        print(f"[WeWorkRemotely] Erreur lors du scraping : {e}")

    return jobs

def extract_email_from_job(job_url):
    try:
        resp = requests.get(job_url)
        soup = BeautifulSoup(resp.text, "html.parser")
        text = soup.get_text()
        import re
        m = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-z]{2,}", text)
        if m:
            return m.group(0)
    except:
        return None
    return None
