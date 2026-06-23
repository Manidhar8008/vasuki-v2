from db.connection import get_conn


def search_personal_memory(query: str, limit: int = 5) -> list[dict]:
    terms = [term.strip().lower() for term in query.split() if len(term.strip()) >= 3]

    if not terms:
        return []

    conn = get_conn()

    clauses = " OR ".join(["LOWER(memory_chunks.content) LIKE ?"] * len(terms))
    values = [f"%{term}%" for term in terms]

    rows = conn.execute(
        f"""
        SELECT
            memory_chunks.id,
            memory_chunks.content,
            imported_documents.source_path
        FROM memory_chunks
        JOIN imported_documents
            ON imported_documents.id = memory_chunks.document_id
        WHERE {clauses}
        ORDER BY memory_chunks.id DESC
        LIMIT ?
        """,
        (*values, limit)
    ).fetchall()

    conn.close()

    return [
        {
            "source": row["source_path"],
            "content": row["content"]
        }
        for row in rows
    ]
