import gspread
from gspread.exceptions import SpreadsheetNotFound

def connect_sheets(json_file, sheet_name):
    client = gspread.service_account(json_file)
    try:
        sheet = client.open(sheet_name).sheet1
        print(f"✅ Connecté au Google Sheet '{sheet_name}'")
    except SpreadsheetNotFound:
        raise Exception(
            f"⚠️ Google Sheet '{sheet_name}' introuvable. "
            "Vérifie le nom exact et que le service account a accès."
        )
    return sheet

def append_row(sheet, data):
    try:
        sheet.append_row(data)
        print("🗂 Ligne ajoutée dans Google Sheet.")
    except Exception as e:
        print(f"[Sheets] Erreur lors de l'ajout de ligne : {e}")

def save_job(sheet, job, language):
    """
    Sauvegarde une offre dans Google Sheets.
    """
    from datetime import datetime
    row = [
        job.get("title", ""),
        job.get("company", ""),
        job.get("source", ""),
        job.get("url", ""),
        language.upper(),
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ]
    append_row(sheet, row)
