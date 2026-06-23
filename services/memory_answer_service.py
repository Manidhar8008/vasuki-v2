from services.personal_memory_service import search_personal_memory, repeated_topics


def answer_from_memory(query: str) -> dict:
    matches = search_personal_memory(query, limit=5)

    if not matches:
        return {
            "tool": "personal_memory",
            "query": query,
            "count": 0,
            "answer": "I could not find approved local memory relevant to that question.",
            "evidence": [],
            "topic_summary": {},
        }

    evidence = []
    seen = set()

    for match in matches:
        source = match.get("source", "unknown source")
        content = " ".join(match.get("content", "").split())

        key = (source, content[:180])
        if key in seen:
            continue
        seen.add(key)

        evidence.append(
            {
                "source": source,
                "excerpt": content[:350],
                "score": match.get("score", 0),
                "matched_terms": match.get("matched_terms", []),
            }
        )

    summary = repeated_topics(query)

    answer = (
        f"I found {len(evidence)} relevant approved memory chunk(s). "
        f"Most relevant terms: "
        f"{', '.join(item['term'] for item in summary['topic_terms'][:3]) or 'none'}."
    )

    return {
        "tool": "personal_memory",
        "query": query,
        "count": len(evidence),
        "answer": answer,
        "evidence": evidence,
        "topic_summary": summary,
    }
