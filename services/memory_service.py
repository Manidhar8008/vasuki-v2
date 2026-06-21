from db.memory_view import MemoryView

def search_memory(query: str, limit: int = 5) -> dict:
    memory = MemoryView()
    results = memory.get_context(query)

    return {
        "tool": "memory_search",
        "query": query,
        "count": min(len(results), limit),
        "results": results[:limit]
    }
