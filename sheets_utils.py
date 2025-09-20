import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

def connect_sheets(json_keyfile, sheet_name):
    scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',
             "https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(json_keyfile, scope)
    client = gspread.authorize(creds)
    try:
        sheet = client.open(sheet_name).sheet1
        return sheet
    except gspread.SpreadsheetNotFound:
        raise Exception(f"⚠️ Google Sheet '{sheet_name}' introuvable. Vérifie le nom exact et que le service account a accès.")

def save_job(sheet, job, lang):
    try:
        # Vérifie doublon via URL
        all_urls = sheet.col_values(4)
        if job.get("url") in all_urls:
            print(f"🗂 Offre déjà enregistrée ({job.get('title')})")
            return
        sheet.append_row([
            job.get("title"),
            job.get("company"),
            job.get("apply_email"),
            job.get("url"),
            lang.upper(),
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ])
        print(f"🗂 Offre enregistrée dans Google Sheets ({job.get('title')})")
    except Exception as e:
        print(f"[Notion] Erreur sauvegarde : {e}")
