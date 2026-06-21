from datetime import datetime, timezone
from db.connection import get_conn

class EventStore:
    def __init__(self):
        self.conn = get_conn()

    def emit(self, event_type: str, key: str, value: str) -> None:
        ts = datetime.now(timezone.utc).isoformat()
        event = f"{event_type}|{key}|{value}"

        self.conn.execute(
            "INSERT INTO event_log (ts, event) VALUES (?, ?)",
            (ts, event),
        )
        self.conn.commit()

    def fetch(self, limit: int = 100):
        rows = self.conn.execute(
            "SELECT id, ts, event FROM event_log ORDER BY id DESC LIMIT ?",
            (limit,),
        ).fetchall()
        return rows
