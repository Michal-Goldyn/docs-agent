CREATE EXTENSION IF NOT EXISTS vector;
CREATE TABLE documents(
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    source TEXT NOT NULL,
    title TEXT,
    ver TEXT NOT NULL,
    lang TEXT NOT NULL DEFAULT 'en',
    content_hash TEXT NOT NULL,
    indexed_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE(source, ver, lang)
);
CREATE TABLE chunks(
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    document_id BIGINT NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
    position int NOT NULL,
    section TEXT,
    content TEXT NOT NULL,
    tokens int,
    embedding VECTOR(1536) NOT NULL,
    UNIQUE (document_id, position)
);