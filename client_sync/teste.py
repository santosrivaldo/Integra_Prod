import sqlite3

DB_PATH = r"C:\Users\rival\AppData\Local\activitywatch\activitywatch\aw-server\peewee-sqlite.v2.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute("PRAGMA table_info(bucketmodel);")
columns = cursor.fetchall()

print("Colunas da tabela bucketmodel:")
for col in columns:
    print(f"- {col[1]} ({col[2]})")

conn.close()
