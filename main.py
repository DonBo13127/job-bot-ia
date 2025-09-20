from scraper import scrape_all

def main():
    print("🚀 Démarrage du bot de candidature automatique...\n")

    # ===========================
    #  Étape 1 : Collecte des jobs
    # ===========================
    print("🔍 Collecte des offres d'emploi...")
    jobs = scrape_all()

    if not jobs:
        print("📭 Aucune offre trouvée. Fin du processus.")
        return

    print(f"✅ {len(jobs)} offres collectées.\n")

    # ===========================
    #  Étape 2 : Affichage des jobs
    # ===========================
    for i, job in enumerate(jobs, 1):
        print(f"\n--- Offre {i}/{len(jobs)} ---")
        print(f"💼 {job.get('title', 'Sans titre')} chez {job.get('company', 'Inconnu')} ({job.get('source', 'N/A')})")
        print(f"🌍 Localisation : {job.get('location', 'Non précisée')}")
        print(f"🔗 {job.get('url', 'Pas de lien')}")

    # ===========================
    #  Étape 3 : Actions futures
    # ===========================
    # Ici, tu pourras :
    # - stocker les jobs dans Notion (via notion_db.py)
    # - générer un message de candidature avec gpt_generator.py
    # - envoyer les candidatures avec email_sender.py
    # Pour l’instant, le bot ne fait qu’afficher les résultats.
    print("\n🎯 Processus terminé.")


if __name__ == "__main__":
    main()
