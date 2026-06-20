import sqlite3
import time
from core.config import DB_PATH


class EventStore:
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row

    def emit(self, event_type, key="", value=""):
        ts = int(time.time())

        self.conn.execute(
            "INSERT INTO event_log (ts, event) VALUES (?, ?)",
            (ts, f"{event_type}|{key}|{value}")
        )
        self.conn.commit()

    def fetch(self, limit=200):
        cur = self.conn.execute(
            "SELECT * FROM event_log ORDER BY id DESC LIMIT ?",
            (limit,)
        )
        return cur.fetchall()
