import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

def connect_sheets(json_keyfile, sheet_url_or_id):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(json_keyfile, scope)
    client = gspread.authorize(creds)

    try:
        sheet = client.open_by_url(sheet_url_or_id).sheet1
        return sheet
    except Exception:
        try:
            sheet = client.open_by_key(sheet_url_or_id).sheet1
            return sheet
        except Exception:
            raise Exception(f"⚠️ Google Sheet '{sheet_url_or_id}' introuvable. Vérifie que le service account a accès.")

def save_job(sheet, job, lang):
    try:
        sheet.append_row([
            job.get("title", ""),
            job.get("company", ""),
            job.get("source", ""),
            job.get("apply_email", ""),
            lang.upper(),
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ])
        print(f"🗂 Offre enregistrée dans Google Sheets ({job.get('title')})")
    except Exception as e:
        print(f"[Sheets] Erreur : {e}")
