import re
from collections import Counter
from db.connection import get_conn

STOP_WORDS = {
    "what", "have", "said", "about", "that", "this", "with", "from",
    "your", "you", "the", "and", "for", "are", "was", "were", "into",
    "want", "need", "does", "did", "who", "why", "how", "when",
}


def extract_terms(query: str) -> list[str]:
    words = re.findall(r"[a-zA-Z0-9_+-]+", query.lower())
    terms = [
        word for word in words
        if len(word) >= 3 and word not in STOP_WORDS
    ]
    return list(dict.fromkeys(terms))


def search_personal_memory(query: str, limit: int = 5) -> list[dict]:
    terms = extract_terms(query)

    if not terms:
        return []

    conn = get_conn()

    clauses = " OR ".join(
        ["LOWER(memory_chunks.content) LIKE ?"] * len(terms)
    )
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
        LIMIT 100
        """,
        values,
    ).fetchall()

    conn.close()

    ranked = []

    for row in rows:
        content = row["content"]
        lowered = content.lower()

        hits = sum(lowered.count(term) for term in terms)
        unique_hits = sum(1 for term in terms if term in lowered)
        score = (unique_hits * 10) + hits

        ranked.append(
            {
                "source": row["source_path"],
                "content": content,
                "score": score,
                "matched_terms": [
                    term for term in terms if term in lowered
                ],
            }
        )

    ranked.sort(
        key=lambda item: (item["score"], len(item["content"])),
        reverse=True,
    )

    return ranked[:limit]


def repeated_topics(query: str, limit: int = 5) -> dict:
    matches = search_personal_memory(query, limit=50)

    source_counts = Counter(match["source"] for match in matches)
    term_counts = Counter(
        term
        for match in matches
        for term in match["matched_terms"]
    )

    return {
        "query": query,
        "matching_chunks": len(matches),
        "source_counts": dict(source_counts.most_common(limit)),
        "topic_terms": [
            {"term": term, "mentions": count}
            for term, count in term_counts.most_common(limit)
        ],
    }
