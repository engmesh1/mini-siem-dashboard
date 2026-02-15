from __future__ import annotations

import re
from datetime import datetime, timezone
from typing import Any, Mapping

from dateutil import parser

_ipv4 = re.compile(r"^\d{1,3}(?:\.\d{1,3}){3}$")

def _safe_parse_ts(value: str) -> str:
    # Accept ISO strings; convert to UTC Z form for consistency.
    dt = parser.isoparse(value)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    dt = dt.astimezone(timezone.utc)
    return dt.replace(microsecond=0).isoformat().replace("+00:00", "Z")

def normalize_event(payload: Mapping[str, Any]) -> dict[str, Any]:
    # Extract known fields; keep original as raw.
    raw = dict(payload)

    timestamp = raw.get("timestamp") or raw.get("@timestamp")
    if not timestamp:
        # fallback: now
        timestamp = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    timestamp = _safe_parse_ts(str(timestamp))

    src_ip = raw.get("src_ip") or raw.get("source_ip") or raw.get("src")
    dest_ip = raw.get("dest_ip") or raw.get("destination_ip") or raw.get("dst")

    event_type = raw.get("event_type") or raw.get("type") or raw.get("event") or "unknown"
    event_type = str(event_type).strip().lower()[:64]

    severity = raw.get("severity")
    if severity is None:
        # simple heuristic
        sev_map = {
            "auth_failed": 6,
            "port_scan": 7,
            "malware": 9,
            "dns_query": 2,
        }
        severity = sev_map.get(event_type, 3)
    severity = int(max(0, min(10, int(severity))))

    message = raw.get("message") or raw.get("msg") or raw.get("description")
    message = str(message)[:500] if message is not None else None

    return {
        "timestamp": timestamp,
        "src_ip": str(src_ip)[:64] if src_ip is not None else None,
        "dest_ip": str(dest_ip)[:64] if dest_ip is not None else None,
        "event_type": event_type,
        "severity": severity,
        "message": message,
        "raw": raw,
    }
