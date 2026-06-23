import hashlib
import sqlite3
from pathlib import Path
from db.connection import get_conn


def ensure_knowledge_schema() -> None:
    conn = get_conn()
    conn.executescript("""
    CREATE TABLE IF NOT EXISTS knowledge_sources (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        source_path TEXT UNIQUE NOT NULL,
        source_type TEXT NOT NULL,
        content_hash TEXT NOT NULL,
        size_bytes INTEGER NOT NULL,
        imported_at TEXT DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS knowledge_chunks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        source_id INTEGER NOT NULL,
        chunk_index INTEGER NOT NULL,
        content TEXT NOT NULL,
        FOREIGN KEY(source_id) REFERENCES knowledge_sources(id),
        UNIQUE(source_id, chunk_index)
    );

    CREATE TABLE IF NOT EXISTS knowledge_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        source_id INTEGER NOT NULL,
        chunk_id INTEGER NOT NULL,
        item_type TEXT NOT NULL,
        content TEXT NOT NULL,
        confidence REAL DEFAULT 0.70,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(source_id) REFERENCES knowledge_sources(id),
        FOREIGN KEY(chunk_id) REFERENCES knowledge_chunks(id)
    );

    CREATE TABLE IF NOT EXISTS ingestion_runs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        source_path TEXT NOT NULL,
        status TEXT NOT NULL,
        detail TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    );

    CREATE INDEX IF NOT EXISTS idx_knowledge_chunks_source
        ON knowledge_chunks(source_id);

    CREATE INDEX IF NOT EXISTS idx_knowledge_items_type
        ON knowledge_items(item_type);
    """)
    conn.commit()
    conn.close()


def file_hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(65536), b""):
            digest.update(block)
    return digest.hexdigest()


def get_existing_source(conn: sqlite3.Connection, source_path: str):
    return conn.execute(
        "SELECT id, content_hash FROM knowledge_sources WHERE source_path = ?",
        (source_path,),
    ).fetchone()
