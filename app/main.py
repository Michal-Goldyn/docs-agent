from app.config import settings
from app.search import search_chunks
from app.answer import answer
from fastapi import FastAPI
import psycopg

app = FastAPI(title="Docs Agent", description="RAG agent for FastAPI documentation", version="0.1.0")

@app.get("/ping")
def ping():
    """Return OK if the API is running."""
    return {"status": "ok"}

@app.get("/health")
def check_connection():
    """Verify the database connection is working."""
    with psycopg.connect(settings.database_url) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT 1")
            result = cur.fetchone()
    return {"db": "ok", "result": result}

@app.get("/search")
def search(q: str):
    """Search the documentation for chunks relevant to the question."""
    return search_chunks(q)

@app.get("/ask")
def ask(q: str):
    """Answer a question about FastAPI docs using retrieved context."""
    return {"answer": answer(q)}