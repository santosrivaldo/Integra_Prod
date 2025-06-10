# api/main.py
from fastapi import FastAPI, Depends
from typing import List
import psycopg2
import os
import time
from models import Activity
from auth import validate_token
from utils import create_table_if_not_exists

app = FastAPI()

# Função de conexão com retries
def connect_to_db():
    for attempt in range(10):
        try:
            conn = psycopg2.connect(
                dbname=os.getenv("POSTGRES_DB", "productivity"),
                user=os.getenv("POSTGRES_USER", "user"),
                password=os.getenv("POSTGRES_PASSWORD", "password"),
                host=os.getenv("POSTGRES_HOST", "db")
            )
            print("✅ Conexão com o banco bem-sucedida.")
            return conn
        except psycopg2.OperationalError as e:
            print(f"⏳ Tentativa {attempt + 1}/10 falhou: {e}")
            time.sleep(3)
    raise Exception("❌ Falha ao conectar no banco após múltiplas tentativas.")

conn = connect_to_db()
cursor = conn.cursor()
create_table_if_not_exists(cursor)

@app.post("/sync")
async def sync_activities(data: List[Activity], _: str = Depends(validate_token)):
    for activity in data:
        cursor.execute(
            """
            INSERT INTO activities (username, appname, start_time, end_time, active, bucket, timestamp)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (
                activity.user,
                activity.app,
                activity.start,
                activity.end,
                activity.active,
                activity.bucket,
                activity.timestamp
            )
        )
    conn.commit()
    return {"status": "success"}

@app.get("/report")
def report():
    cursor.execute("SELECT username, appname, bucket, start_time, end_time FROM activities ORDER BY timestamp DESC LIMIT 100")
    result = cursor.fetchall()
    return [
        {
            "user": r[0],
            "app": r[1],
            "bucket": r[2],
            "start": r[3],
            "end": r[4]
        } for r in result
    ]
