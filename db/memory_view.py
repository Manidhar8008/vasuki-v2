from db.event_store import EventStore


class MemoryView:
    def __init__(self):
        self.store = EventStore()

    def get_context(self, query, limit=10):
        rows = self.store.fetch(500)

        seen = set()
        scored = []

        for r in rows:
            event = r["event"]

            if query.lower() in event.lower():

                if event in seen:
                    continue
                seen.add(event)

                parts = event.split("|")

                score = 1
                if "USER_QUERY" not in event:
                    score += 2
                if len(event) > 20:
                    score += 1

                scored.append({
                    "type": parts[0] if len(parts) > 0 else "",
                    "key": parts[1] if len(parts) > 1 else "",
                    "value": parts[2] if len(parts) > 2 else "",
                    "score": score
                })

        scored.sort(key=lambda x: x["score"], reverse=True)
        return scored[:limit]
