from app.config import settings
from app.search import search_chunks
from fastapi import FastAPI
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

@app.get("/search")
def search(q: str):
    return search_chunks(q)
