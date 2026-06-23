from services.memory_service import search_memory


def general_reasoning(query: str) -> dict:
    memory_result = search_memory(query, limit=5)
    matches = memory_result.get("results", [])

    if matches:
        answer = "I found matching local memory records."
    else:
        answer = (
            "I do not have a verified answer yet. "
            "Use a more specific request, or add information to Vasuki memory first."
        )

    return {
        "tool": "general_reasoning",
        "query": query,
        "answer": answer,
        "memory_matches": matches,
    }
