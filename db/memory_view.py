from db.event_store import EventStore

class MemoryView:
    def __init__(self):
        self.store = EventStore()

    def get_context(self, query, limit=10):
        rows = self.store.fetch(500)
        results = []

        for r in rows:
            event = r["event"]
            if query.lower() in event.lower():
                parts = event.split("|")

                results.append({
                    "type": parts[0],
                    "key": parts[1],
                    "value": parts[2],
                    "score": 1
                })

        return results[:limit]
