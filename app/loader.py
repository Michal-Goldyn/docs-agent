from app.config import settings
from pathlib import Path
import hashlib
import psycopg

def md_files(directory: Path):
    p_glob = directory.rglob('*.md')
    return p_glob

def get_one_file(directory: Path):
    p = directory
    with p.open(encoding="utf-8") as f:
        content = f.read()

    title = content.splitlines()[0].lstrip("#").split("{")[0].strip()
    source = p.relative_to(settings.docs_path).as_posix()
    content_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()

    return {"source": source, "title": title, "content_hash": content_hash}

def save_one_to_database(doc: dict):
    with psycopg.connect(settings.database_url) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO documents (source, title, ver, lang, content_hash)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (source, ver, lang) DO NOTHING
            """, (doc["source"], doc["title"], "0.115", "en", doc["content_hash"]))

if __name__ == "__main__":
    files = list(md_files(settings.docs_path))
    for f in files:
        doc = get_one_file(f)
        save_one_to_database(doc)
        print(doc["source"])