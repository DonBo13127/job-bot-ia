import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

def connect_sheets(json_file, sheet_url):
    scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',
             "https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(json_file, scope)
    client = gspread.authorize(creds)

    # Extraire l'ID du sheet depuis l'URL
    sheet_id = sheet_url.split("/d/")[1].split("/")[0]
    try:
        sheet = client.open_by_key(sheet_id).sheet1
        return sheet
    except Exception as e:
        raise Exception(f"⚠️ Google Sheet introuvable ou accès refusé : {e}")

def save_job(sheet, job, language):
    # Vérifier doublon
    existing = sheet.col_values(2)  # colonne URL
    if job["url"] in existing:
        return False
    sheet.append_row([
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        job["url"],
        job["title"],
        job["company"],
        job["apply_email"],
        language.upper()
    ])
    return True
