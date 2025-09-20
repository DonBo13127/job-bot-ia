# sheets_utils.py
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def connect_sheets(json_file, sheet_name, worksheet_index=0):
    """
    Connexion à Google Sheets via un service account.
    """
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_name(json_file, scope)
    client = gspread.authorize(creds)
    
    try:
        sheet = client.open(sheet_name).get_worksheet(worksheet_index)
        return sheet
    except gspread.SpreadsheetNotFound:
        raise Exception(
            f"⚠️ Google Sheet '{sheet_name}' introuvable. "
            "Vérifie le nom exact et que le service account a accès (partagez le mail du service account avec la feuille)."
        )

def save_job(sheet, job, language):
    """
    Sauvegarde une offre dans la sheet si elle n'existe pas déjà.
    """
    records = sheet.get_all_records()
    title = job.get("title", "")
    company = job.get("company", "")
    url = job.get("url", "")

    # Vérifie doublon via URL
    if any(r.get("URL") == url for r in records):
        print(f"🔹 Offre déjà enregistrée : {title} ({company})")
        return

    row = [
        title,
        company,
        job.get("source", ""),
        url,
        language.upper()
    ]
    sheet.append_row(row)
    print(f"🗂 Offre enregistrée dans Google Sheets ({title})")
