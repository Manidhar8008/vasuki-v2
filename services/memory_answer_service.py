from services.personal_memory_service import search_personal_memory


def answer_from_memory(query: str) -> dict:
    matches = search_personal_memory(query)

    if not matches:
        return {
            "tool": "personal_memory",
            "query": query,
            "count": 0,
            "answer": "I could not find approved local memory relevant to that question.",
            "evidence": [],
        }

    evidence = []
    seen = set()

    for match in matches[:5]:
        source = match.get("source", "unknown source")
        content = " ".join(match.get("content", "").split())

        key = (source, content[:180])
        if key in seen:
            continue
        seen.add(key)

        evidence.append({
            "source": source,
            "excerpt": content[:350],
        })

    answer = (
        f"I found {len(evidence)} relevant approved memory chunk(s). "
        "Here is the evidence from your local imports."
    )

    return {
        "tool": "personal_memory",
        "query": query,
        "count": len(evidence),
        "answer": answer,
        "evidence": evidence,
    }
