from fastapi import FastAPI
from app.config import settings
import psycopg

app = FastAPI()

@app.get("/ping")
def ping():
    return {"status": "ok"}

@app.get("/health")
def check_connection():
    with psycopg.connect(settings.database_url) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT 1")
            result = cur.fetchone()
    return {"db": "ok", "result": result}