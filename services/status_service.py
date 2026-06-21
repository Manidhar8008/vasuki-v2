from db.connection import get_conn

def get_status() -> dict:
    conn = get_conn()
    cursor = conn.cursor()

    tables = cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
    ).fetchall()

    event_count = cursor.execute(
        "SELECT COUNT(*) FROM event_log"
    ).fetchone()[0]

    conn.close()

    return {
        "tool": "system_status",
        "database": "connected",
        "tables": [row[0] for row in tables],
        "event_count": event_count,
    }
