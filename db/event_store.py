from db.connection import get_conn
from datetime import datetime

class EventStore:
    def __init__(self):
        self.conn = get_conn()

    def emit(self, event_type, key, value):
        ts = datetime.utcnow().isoformat()

        self.conn.execute("""
            INSERT INTO event_log (ts, event)
            VALUES (?, ?)
        """, (ts, f"{event_type}|{key}|{value}"))

        self.conn.commit()

    def fetch(self, limit=100):
        cur = self.conn.execute("""
            SELECT * FROM event_log
            ORDER BY id DESC
            LIMIT ?
        """, (limit,))
        return cur.fetchall()
