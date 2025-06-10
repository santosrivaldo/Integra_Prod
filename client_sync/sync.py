# client_sync/sync.py

import sqlite3
import json
import requests
import os
import time
import logging
from datetime import datetime, timedelta

API_URL = os.getenv("API_URL", "http://localhost:5000/sync")
API_KEY = os.getenv("API_KEY", "my_secure_token")
DB_PATH = os.path.expanduser("~\\AppData\\Local\\activitywatch\\activitywatch\\aw-server\\peewee-sqlite.v2.db")
HEADERS = {"Authorization": f"Bearer {API_KEY}"}
USERNAME = os.getenv("USERNAME", os.getlogin())

def extract_events():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT e.timestamp, e.duration, e.datastr, b.id
        FROM eventmodel e
        JOIN bucketmodel b ON e.bucket_id = b.key
        WHERE b.id LIKE 'aw-watcher-window%'
        ORDER BY e.timestamp DESC
        LIMIT 100
    """)

    events = []
    for timestamp, duration, datastr, bucket_id in cursor.fetchall():
        try:
            data = json.loads(datastr)
        except Exception:
            continue

        # Calcular 'end' usando duration em segundos
        start_dt = datetime.fromisoformat(timestamp)
        end_dt = start_dt + timedelta(seconds=float(duration))

        events.append({
            "user": USERNAME,
            "app": data.get("app", "unknown"),
            "start": start_dt.isoformat(),
            "end": end_dt.isoformat(),
            "active": True,
            "bucket": bucket_id,
            "timestamp": datetime.now().isoformat()
        })

    conn.close()
    return events

def sync_data():
    data = extract_events()
    if not data:
        print("Nenhum evento encontrado.")
        return

    try:
        r = requests.post(API_URL, json=data, headers=HEADERS)
        print(f"Enviados {len(data)} eventos. Status: {r.status_code}")
        print(r.text)
    except Exception as e:
        print("Erro ao enviar dados:", e)

def agendador_sync():
    while True:
        try:
            print("Executando sincronização...")
            sync_data()
            print("Sincronização concluída.")
        except Exception as e:
            logging.exception("Erro durante sincronização:")
        time.sleep(3600)  # Espera 1 hora (3600 segundos)


if __name__ == "__main__":
   agendador_sync()
