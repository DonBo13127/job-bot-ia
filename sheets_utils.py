# sheets_utils.py
import gspread
from gspread.exceptions import SpreadsheetNotFound

def connect_sheets(json_file, sheet_name):
    """
    Connexion à Google Sheets via service account.
    Si le sheet n'existe pas, lève une erreur claire.
    """
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
    """
    Ajoute une ligne dans le sheet.
    data doit être une liste correspondant aux colonnes.
    """
    try:
        sheet.append_row(data)
        print("🗂 Ligne ajoutée dans Google Sheet.")
    except Exception as e:
        print(f"[Sheets] Erreur lors de l'ajout de ligne : {e}")
