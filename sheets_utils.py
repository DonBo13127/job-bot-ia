import gspread
from oauth2client.service_account import ServiceAccountCredentials

def connect_sheets(json_keyfile, sheet_url):
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(json_keyfile, scope)
    client = gspread.authorize(creds)
    try:
        sheet = client.open_by_url(sheet_url).sheet1
        return sheet
    except Exception as e:
        raise Exception(f"⚠️ Impossible de se connecter à Google Sheet : {e}")

def save_job(sheet, job):
    """
    Enregistre l'offre dans Google Sheets si elle n'existe pas déjà
    """
    existing = sheet.col_values(1)
    if job['title'] not in existing:
        sheet.append_row([
            job['title'], job.get('company', ''), job['email'], job['url']
        ])
