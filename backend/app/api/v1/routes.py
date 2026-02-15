from __future__ import annotations

import csv
import io
import json
from typing import Any, Optional

from fastapi import APIRouter, Response
from fastapi.responses import StreamingResponse
from pydantic import TypeAdapter

from app.db.database import get_conn, init_db, insert_events
from app.models.schemas import EventsPage, IngestBatch, IngestEvent
from app.services.normalize import normalize_event

router = APIRouter()

@router.get("/healthz")
def healthz() -> dict[str, str]:
    return {"status": "ok"}

@router.post("/ingest")
def ingest(event: IngestEvent) -> dict[str, Any]:
    conn = get_conn()
    init_db(conn)
    normalized = normalize_event(event.model_dump())
    n = insert_events(conn, [normalized])
    return {"inserted": n, "event_type": normalized["event_type"], "severity": normalized["severity"]}

@router.post("/ingest/batch")
def ingest_batch(batch: list[dict[str, Any]] | IngestBatch) -> dict[str, Any]:
    # Accept either {"events":[...]} or a raw list [...]
    if isinstance(batch, IngestBatch):
        events = [e.model_dump() for e in batch.events]
    else:
        events = batch

    conn = get_conn()
    init_db(conn)
    normalized = [normalize_event(e) for e in events]
    n = insert_events(conn, normalized)
    return {"inserted": n}

@router.get("/events", response_model=EventsPage)
def list_events(
    limit: int = 50,
    offset: int = 0,
    event_type: Optional[str] = None,
    src_ip: Optional[str] = None,
    dest_ip: Optional[str] = None,
    severity_min: Optional[int] = None,
    severity_max: Optional[int] = None,
    start_ts: Optional[str] = None,
    end_ts: Optional[str] = None,
) -> EventsPage:
    limit = max(1, min(200, limit))
    offset = max(0, offset)

    where = []
    params: list[Any] = []

    if event_type:
        where.append("event_type = ?")
        params.append(event_type.strip().lower())
    if src_ip:
        where.append("src_ip = ?")
        params.append(src_ip.strip())
    if dest_ip:
        where.append("dest_ip = ?")
        params.append(dest_ip.strip())
    if severity_min is not None:
        where.append("severity >= ?")
        params.append(int(severity_min))
    if severity_max is not None:
        where.append("severity <= ?")
        params.append(int(severity_max))
    if start_ts:
        where.append("timestamp >= ?")
        params.append(start_ts)
    if end_ts:
        where.append("timestamp <= ?")
        params.append(end_ts)

    where_sql = (" WHERE " + " AND ".join(where)) if where else ""
    conn = get_conn()
    init_db(conn)

    total = conn.execute(f"SELECT COUNT(*) as c FROM events{where_sql}", params).fetchone()["c"]

    rows = conn.execute(
        f"""SELECT id, timestamp, src_ip, dest_ip, event_type, severity, message, raw_json
        FROM events{where_sql}
        ORDER BY timestamp DESC
        LIMIT ? OFFSET ?""",
        params + [limit, offset],
    ).fetchall()

    items = []
    for r in rows:
        items.append({
            "id": r["id"],
            "timestamp": r["timestamp"],
            "src_ip": r["src_ip"],
            "dest_ip": r["dest_ip"],
            "event_type": r["event_type"],
            "severity": r["severity"],
            "message": r["message"],
            "raw": json.loads(r["raw_json"]),
        })

    return EventsPage(total=total, limit=limit, offset=offset, items=items)

@router.get("/events/export.csv")
def export_csv(
    event_type: Optional[str] = None,
    src_ip: Optional[str] = None,
    dest_ip: Optional[str] = None,
    severity_min: Optional[int] = None,
    severity_max: Optional[int] = None,
    start_ts: Optional[str] = None,
    end_ts: Optional[str] = None,
) -> StreamingResponse:
    # Reuse list query logic by building WHERE.
    where = []
    params: list[Any] = []

    if event_type:
        where.append("event_type = ?")
        params.append(event_type.strip().lower())
    if src_ip:
        where.append("src_ip = ?")
        params.append(src_ip.strip())
    if dest_ip:
        where.append("dest_ip = ?")
        params.append(dest_ip.strip())
    if severity_min is not None:
        where.append("severity >= ?")
        params.append(int(severity_min))
    if severity_max is not None:
        where.append("severity <= ?")
        params.append(int(severity_max))
    if start_ts:
        where.append("timestamp >= ?")
        params.append(start_ts)
    if end_ts:
        where.append("timestamp <= ?")
        params.append(end_ts)

    where_sql = (" WHERE " + " AND ".join(where)) if where else ""
    conn = get_conn()
    init_db(conn)

    rows = conn.execute(
        f"""SELECT id, timestamp, src_ip, dest_ip, event_type, severity, message
        FROM events{where_sql}
        ORDER BY timestamp DESC""",
        params,
    ).fetchall()

    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow(["id", "timestamp", "src_ip", "dest_ip", "event_type", "severity", "message"])
    for r in rows:
        writer.writerow([r["id"], r["timestamp"], r["src_ip"], r["dest_ip"], r["event_type"], r["severity"], r["message"]])

    buf.seek(0)
    return StreamingResponse(
        iter([buf.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=events.csv"},
    )
