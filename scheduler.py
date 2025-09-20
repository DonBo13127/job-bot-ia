import time
import subprocess

while True:
    print("⏰ Lancement du bot de candidature...")
    subprocess.run(["python", "main.py"])
    print("🕐 Attente 1 heure avant la prochaine exécution...")
    time.sleep(3600)  # 1 heure
