import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

def connect_sheets_by_id(json_file, spreadsheet_id, worksheet_index=0):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(json_file, scope)
    client = gspread.authorize(creds)
    try:
        sheet = client.open_by_key(spreadsheet_id).get_worksheet(worksheet_index)
        return sheet
    except Exception as e:
        raise Exception(f"⚠️ Google Sheet introuvable ou accès refusé : {e}")

def save_job_to_sheet(sheet, job, language="FR"):
    try:
        sheet.append_row([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            job.get("title", ""),
            job.get("company", ""),
            job.get("source", ""),
            job.get("url", ""),
            language.upper()
        ])
        print(f"🗂 Offre enregistrée : {job.get('title')}")
    except Exception as e:
        print(f"[Sheets] Erreur : {e}")
