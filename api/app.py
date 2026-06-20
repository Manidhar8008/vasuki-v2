from db.event_store import EventStore
from db.memory_view import MemoryView

class AskAPI:
    def __init__(self):
        self.store = EventStore()
        self.memory = MemoryView()

    def ask(self, query: str):
        self.store.emit("USER_QUERY", "ask", query)

        memories = self.memory.get_context(query)

        if not memories:
            return {
                "query": query,
                "top_memories": [],
                "count": 0
            }

        return {
            "query": query,
            "top_memories": memories,
            "count": len(memories)
        }
