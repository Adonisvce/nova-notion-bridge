
from apscheduler.schedulers.background import BackgroundScheduler
import requests
import os

def schedule_auto_sync():
    def sync_logic():
        try:
            url = os.getenv("SELF_SYNC_ENDPOINT", "https://nova.novaaisecurity.com/sync-logic")
            response = requests.post(url)
            print(f"[AUTO-SYNC] {response.json()}")
        except Exception as e:
            print(f"[AUTO-SYNC ERROR] {e}")

    scheduler = BackgroundScheduler()
    scheduler.add_job(sync_logic, 'interval', minutes=10)
    scheduler.start()
