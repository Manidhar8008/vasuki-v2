from pathlib import Path
from db.connection import get_conn
from db.knowledge_store import ensure_knowledge_schema, file_hash, get_existing_source

IMPORT_DIR = Path("data/private_imports/chatgpt/text")
ALLOWED_EXTENSIONS = {".txt", ".md"}
CHUNK_SIZE = 1200


def chunk_text(text: str) -> list[str]:
    text = text.replace("\r\n", "\n").strip()
    if not text:
        return []

    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks = []
    current = ""

    for paragraph in paragraphs:
        candidate = f"{current}\n\n{paragraph}".strip()
        if len(candidate) <= CHUNK_SIZE:
            current = candidate
        else:
            if current:
                chunks.append(current)
            current = paragraph

    if current:
        chunks.append(current)

    return chunks


def classify_line(line: str):
    value = line.strip()
    lower = value.lower()

    if not value:
        return None

    if any(word in lower for word in ["my goal", "i want", "i need", "aim is", "immediate goal"]):
        return "goal"

    if any(word in lower for word in ["decided", "decision", "we will", "we should", "next step"]):
        return "decision"

    if any(word in lower for word in ["error", "problem", "not working", "failed", "issue", "traceback"]):
        return "problem"

    if any(word in lower for word in ["fixed", "solution", "resolved", "works now", "working now"]):
        return "solution"

    return None


def import_file(path: Path) -> str:
    source_path = str(path)
    content = path.read_text(encoding="utf-8", errors="ignore")
    content_hash = file_hash(path)
    chunks = chunk_text(content)

    conn = get_conn()
    existing = get_existing_source(conn, source_path)

    if existing and existing["content_hash"] == content_hash:
        conn.execute(
            "INSERT INTO ingestion_runs(source_path, status, detail) VALUES (?, ?, ?)",
            (source_path, "skipped", "unchanged"),
        )
        conn.commit()
        conn.close()
        return f"SKIP unchanged: {path.name}"

    if existing:
        conn.execute("DELETE FROM knowledge_items WHERE source_id = ?", (existing["id"],))
        conn.execute("DELETE FROM knowledge_chunks WHERE source_id = ?", (existing["id"],))
        conn.execute("DELETE FROM knowledge_sources WHERE id = ?", (existing["id"],))

    cursor = conn.execute(
        """
        INSERT INTO knowledge_sources(source_path, source_type, content_hash, size_bytes)
        VALUES (?, ?, ?, ?)
        """,
        (source_path, "text", content_hash, path.stat().st_size),
    )
    source_id = cursor.lastrowid

    item_count = 0
    for index, chunk in enumerate(chunks):
        cursor = conn.execute(
            """
            INSERT INTO knowledge_chunks(source_id, chunk_index, content)
            VALUES (?, ?, ?)
            """,
            (source_id, index, chunk),
        )
        chunk_id = cursor.lastrowid

        for line in chunk.splitlines():
            item_type = classify_line(line)
            if item_type:
                conn.execute(
                    """
                    INSERT INTO knowledge_items(source_id, chunk_id, item_type, content)
                    VALUES (?, ?, ?, ?)
                    """,
                    (source_id, chunk_id, item_type, line.strip()),
                )
                item_count += 1

    conn.execute(
        "INSERT INTO ingestion_runs(source_path, status, detail) VALUES (?, ?, ?)",
        (source_path, "imported", f"chunks={len(chunks)}, items={item_count}"),
    )
    conn.commit()
    conn.close()

    return f"IMPORTED {path.name}: {len(chunks)} chunks, {item_count} knowledge items"


def main():
    ensure_knowledge_schema()

    if not IMPORT_DIR.exists():
        print(f"Missing import folder: {IMPORT_DIR}")
        return

    files = sorted(
        path for path in IMPORT_DIR.rglob("*")
        if path.is_file() and path.suffix.lower() in ALLOWED_EXTENSIONS
    )

    if not files:
        print("No .txt or .md files found.")
        return

    for path in files:
        try:
            print(import_file(path))
        except Exception as error:
            print(f"FAILED {path.name}: {error}")


if __name__ == "__main__":
    main()
