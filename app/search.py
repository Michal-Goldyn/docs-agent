from app.embeddings import embed
from app.config import settings
import psycopg
from psycopg.rows import dict_row

def search_chunks(question: str):
    q = str(embed(question))
    with psycopg.connect(settings.database_url) as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute("""
                SELECT 
                    c.id,
                    d.title,
                    d.source,
                    c.section,
                    1 - (c.embedding <=> %s::vector) AS similarity,
                    c.content
                FROM chunks AS c
                JOIN documents as d
                    ON c.document_id = d.id
                ORDER by c.embedding <=> %s::vector ASC
                LIMIT 5
            """, (q,q))
            return cur.fetchall()

if __name__ == "__main__":
    for row in search_chunks("How to upload a file in FastAPI"):
        print(row["title"], "|", row["section"], "|", round(row["similarity"], 3))