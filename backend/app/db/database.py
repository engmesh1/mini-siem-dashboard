from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any, Iterable

from app.core.config import settings

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS events (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  timestamp TEXT NOT NULL,
  src_ip TEXT,
  dest_ip TEXT,
  event_type TEXT NOT NULL,
  severity INTEGER NOT NULL,
  message TEXT,
  raw_json TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_events_ts ON events(timestamp);
CREATE INDEX IF NOT EXISTS idx_events_src ON events(src_ip);
CREATE INDEX IF NOT EXISTS idx_events_dest ON events(dest_ip);
CREATE INDEX IF NOT EXISTS idx_events_type ON events(event_type);
CREATE INDEX IF NOT EXISTS idx_events_sev ON events(severity);
"""

def get_conn(db_path: Path | None = None) -> sqlite3.Connection:
    path = db_path or settings.db_path
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(path), check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db(conn: sqlite3.Connection) -> None:
    conn.executescript(SCHEMA_SQL)
    conn.commit()

def insert_events(conn: sqlite3.Connection, rows: Iterable[dict[str, Any]]) -> int:
    cur = conn.cursor()
    payloads = []
    for r in rows:
        payloads.append((
            r["timestamp"],
            r.get("src_ip"),
            r.get("dest_ip"),
            r["event_type"],
            int(r["severity"]),
            r.get("message"),
            json.dumps(r["raw"], ensure_ascii=False),
        ))
    cur.executemany(
        """INSERT INTO events(timestamp, src_ip, dest_ip, event_type, severity, message, raw_json)
        VALUES (?, ?, ?, ?, ?, ?, ?)""",
        payloads,
    )
    conn.commit()
    return cur.rowcount
