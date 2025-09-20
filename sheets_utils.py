import gspread
from oauth2client.service_account import ServiceAccountCredentials

def connect_sheets(json_keyfile_path, sheet_url):
    if not json_keyfile_path:
        raise Exception("⚠️ Chemin du fichier JSON manquant.")

    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive.file",
        "https://www.googleapis.com/auth/drive"
    ]

    creds = ServiceAccountCredentials.from_json_keyfile_name(json_keyfile_path, scope)
    client = gspread.authorize(creds)

    try:
        key = sheet_url.split("/d/")[1].split("/")[0]
        sheet = client.open_by_key(key).sheet1
        return sheet
    except Exception as e:
        raise Exception(f"⚠️ Impossible d'ouvrir le Google Sheet : {e}")

def save_job(sheet, job):
    try:
        sheet.append_row([
            job.get("title"),
            job.get("company"),
            job.get("apply_email"),
            job.get("source"),
            job.get("link"),
            job.get("lang")
        ])
        print(f"🗂 Offre enregistrée : {job.get('title')}")
    except Exception as e:
        print(f"[Sheets] Erreur : {e}")
