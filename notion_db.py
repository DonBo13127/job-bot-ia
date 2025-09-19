# notion_db.py
from notion_client import Client
import os

class NotionDB:
    def __init__(self):
        self.notion = Client(auth=os.getenv("NOTION_API_KEY"))
        self.db_id = os.getenv("NOTION_DATABASE_ID")

    def job_exists(self, job_url):
        """Vérifie si l'offre existe déjà dans Notion"""
        try:
            filter_query = {
                "property": "URL",
                "url": {
                    "equals": job_url
                }
            }
            results = self.notion.databases.query(
                database_id=self.db_id,
                filter=filter_query
            )
            return len(results["results"]) > 0
        except Exception as e:
            print(f"[Notion] Erreur vérification doublon: {e}")
            return False

    def add_job(self, job_data):
        """Ajoute une offre dans Notion"""
        try:
            self.notion.pages.create(
                parent={"database_id": self.db_id},
                properties={
                    "Titre": {"title": [{"text": {"content": job_data['title']}}]},
                    "URL": {"url": job_data['url']},
                    "Entreprise": {"rich_text": [{"text": {"content": job_data.get('company', 'N/A')}}]},
                    "Localisation": {"rich_text": [{"text": {"content": job_data.get('location', 'Remote')}}]},
                    "Langue": {"select": {"name": job_data.get('language', 'fr')}},
                    "Date": {"date": {"start": job_data.get('date_posted', '')}},
                    "Statut": {"select": {"name": "Contacté"}}
                }
            )
            print(f"[Notion] Offre ajoutée : {job_data['title']}")
        except Exception as e:
            print(f"[Notion] Erreur ajout offre : {e}")
