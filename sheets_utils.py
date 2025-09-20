import gspread

def connect_sheets(json_file, sheet_name):
    client = gspread.service_account(json_file)
    sheet = client.open(sheet_name).sheet1
    return sheet

def is_duplicate(sheet, job_title, company):
    records = sheet.get_all_records()
    for r in records:
        if r.get("Titre") == job_title and r.get("Entreprise") == company:
            return True
    return False

def save_job(sheet, job, lang):
    if is_duplicate(sheet, job["title"], job["company"]):
        print(f"🛑 Déjà présent : {job['title']} chez {job['company']}")
        return
    sheet.append_row([job["title"], job["company"], job["source"], job["url"], lang])
    print(f"🗂 Offre enregistrée : {job['title']} chez {job['company']}")
