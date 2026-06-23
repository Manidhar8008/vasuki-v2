from __future__ import annotations

import hashlib
from pathlib import Path

from db.connection import get_conn


IMPORT_ROOT = Path("data/private_imports")
CHUNK_SIZE = 900
OVERLAP = 150


def init_memory_tables() -> None:
    conn = get_conn()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS imported_documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source_path TEXT NOT NULL UNIQUE,
            source_hash TEXT NOT NULL,
            imported_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS memory_chunks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            document_id INTEGER NOT NULL,
            chunk_index INTEGER NOT NULL,
            content TEXT NOT NULL,
            FOREIGN KEY(document_id) REFERENCES imported_documents(id),
            UNIQUE(document_id, chunk_index)
        )
    """)
    conn.commit()
    conn.close()


def chunk_text(text: str) -> list[str]:
    text = " ".join(text.split())
    if not text:
        return []

    chunks = []
    start = 0

    while start < len(text):
        end = min(start + CHUNK_SIZE, len(text))
        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        if end >= len(text):
            break

        start = end - OVERLAP

    return chunks


def import_text_file(path: Path) -> dict:
    init_memory_tables()

    raw = path.read_bytes()
    source_hash = hashlib.sha256(raw).hexdigest()
    text = raw.decode("utf-8", errors="replace")
    chunks = chunk_text(text)

    conn = get_conn()

    existing = conn.execute(
        "SELECT id, source_hash FROM imported_documents WHERE source_path = ?",
        (str(path),)
    ).fetchone()

    if existing and existing["source_hash"] == source_hash:
        conn.close()
        return {
            "path": str(path),
            "status": "unchanged",
            "chunks": 0
        }

    if existing:
        document_id = existing["id"]
        conn.execute("DELETE FROM memory_chunks WHERE document_id = ?", (document_id,))
        conn.execute(
            "UPDATE imported_documents SET source_hash = ?, imported_at = CURRENT_TIMESTAMP WHERE id = ?",
            (source_hash, document_id)
        )
    else:
        cursor = conn.execute(
            "INSERT INTO imported_documents (source_path, source_hash) VALUES (?, ?)",
            (str(path), source_hash)
        )
        document_id = cursor.lastrowid

    for index, chunk in enumerate(chunks):
        conn.execute(
            "INSERT INTO memory_chunks (document_id, chunk_index, content) VALUES (?, ?, ?)",
            (document_id, index, chunk)
        )

    conn.commit()
    conn.close()

    return {
        "path": str(path),
        "status": "imported",
        "chunks": len(chunks)
    }


def import_all_text_files() -> list[dict]:
    if not IMPORT_ROOT.exists():
        return []

    reports = []

    for path in sorted(IMPORT_ROOT.rglob("*.txt")):
        reports.append(import_text_file(path))

    return reports
