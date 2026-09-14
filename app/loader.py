from app.config import settings
from pathlib import Path
import hashlib
import psycopg
import re

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

def expand_code_refs(content: str, docs_root: Path) -> str:
    def replace(match):
        rel_path = match.group(1)
        code_path = (docs_root / rel_path).resolve()
        if not code_path.exists():
            print(f"\nmissing: {code_path}")
            return match.group(0)
        py_file = code_path.read_text(encoding="utf-8")
        return f"```python\n{py_file}\n```"

    return re.sub(r"\{\*\s*(\S+)[^}]*\*\}", replace, content)


def split_by_header(content: str, prefix: str = "## "):
    chunks = []
    current_section = None
    current_lines = []
    in_code_block = False

    for line in content.splitlines():
        if line.startswith("```"):
            in_code_block = not in_code_block
        if line.startswith(prefix) and in_code_block == False:
            text = '\n'.join(current_lines).strip()
            if text:
                chunks.append({
                    "position": len(chunks),
                    "section": current_section,
                    "content": text
                })
            current_lines = []
            current_section = re.sub(r"<[^>]+>", "", line.lstrip("#").split("{")[0]).strip()
            continue
        current_lines.append(line)

    text = "\n".join(current_lines).strip()
    if text:
        chunks.append({
            "position": len(chunks),
            "section": current_section,
            "content": text
        })
    return chunks

def split_into_chunks(content: str, prefix: str = "## ", parent_section: str | None = None):
    results = []
    pending = ""

    split_header = split_by_header(content, prefix)

    for chunk in split_header:
        chunk["section"] = chunk["section"] or parent_section

        if pending:
            chunk["content"] = pending + "\n\n" + chunk["content"]
            pending = ""

        if len(chunk["content"]) < 100:
            pending = chunk["content"]
            continue

        if len(chunk["content"]) <= 2000 or len(prefix) > 5:
            results.append(chunk)
        else:
            results.extend(split_into_chunks(chunk["content"], "#" + prefix, chunk["section"]))

    if pending and results:
        results[-1]["content"] += "\n\n" + pending

    for i, chunk in enumerate(results):
        chunk["position"] = i

    return results



if __name__ == "__main__":
    files = list(md_files(settings.docs_path))
    lengths = []
    test=[]

    for f in files:
        content = f.read_text(encoding="UTF-8")
        content = expand_code_refs(content, settings.docs_root)
        for chunk in split_into_chunks(content):
            lengths.append(len(chunk["content"]))
            if len(chunk["content"]) < 100:
                print(repr(chunk["content"]), "|", chunk["section"])
            if "{*" in chunk["content"]:
                test.append(chunk["content"])
            if len(chunk["content"]) > 5000:
                print(len(chunk["content"]), "|", chunk["section"])
            if chunk["section"] and "<" in chunk["section"]:
                print("HTML w sekcji:", chunk["section"])
    print("fragmentów:", len(lengths))
    print("min:", min(lengths))
    print("max:", max(lengths))
    print("średnia:", sum(lengths) // len(lengths))
    print("powyżej 2000:", len([n for n in lengths if n > 2000]))