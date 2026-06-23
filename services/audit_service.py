from datetime import datetime, timezone
from db.connection import get_conn


def ensure_audit_table() -> None:
    conn = get_conn()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tool_audit_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT NOT NULL,
            capability_id TEXT NOT NULL,
            query TEXT NOT NULL,
            allowed INTEGER NOT NULL,
            outcome TEXT NOT NULL
        )
    """)
    conn.commit()


def record_tool_event(capability_id: str, query: str, allowed: bool, outcome: str) -> None:
    ensure_audit_table()
    conn = get_conn()
    conn.execute(
        """
        INSERT INTO tool_audit_log
        (created_at, capability_id, query, allowed, outcome)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            datetime.now(timezone.utc).isoformat(),
            capability_id,
            query[:500],
            int(allowed),
            outcome[:1000],
        ),
    )
    conn.commit()


def recent_audit(limit: int = 10) -> dict:
    ensure_audit_table()
    conn = get_conn()
    rows = conn.execute(
        """
        SELECT created_at, capability_id, query, allowed, outcome
        FROM tool_audit_log
        ORDER BY id DESC
        LIMIT ?
        """,
        (limit,),
    ).fetchall()

    return {
        "tool": "audit_log",
        "events": [
            {
                "created_at": row[0],
                "capability_id": row[1],
                "query": row[2],
                "allowed": bool(row[3]),
                "outcome": row[4],
            }
            for row in rows
        ],
    }
