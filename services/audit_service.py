from db.event_store import EventStore

def log_action(source: str, action: str, value: str) -> None:
    store = EventStore()
    store.emit("VASUKI_ACTION", f"{source}:{action}", value)
