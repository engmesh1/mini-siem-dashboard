from __future__ import annotations

import os
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.main import app

@pytest.fixture(autouse=True)
def tmp_db(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    db_path = tmp_path / "test.db"
    monkeypatch.setenv("SIEM_DB_PATH", str(db_path))
    yield

def test_ingest_single_and_query():
    client = TestClient(app)

    ev = {
        "timestamp": "2026-02-14T18:23:41Z",
        "src_ip": "1.2.3.4",
        "dest_ip": "10.0.0.1",
        "event_type": "auth_failed",
        "severity": 6,
        "message": "failed login"
    }
    r = client.post("/api/v1/ingest", json=ev)
    assert r.status_code == 200
    assert r.json()["inserted"] == 1

    q = client.get("/api/v1/events?limit=10")
    assert q.status_code == 200
    data = q.json()
    assert data["total"] == 1
    assert data["items"][0]["src_ip"] == "1.2.3.4"

def test_batch_ingest():
    client = TestClient(app)
    batch = [
        {"timestamp": "2026-02-14T18:23:41Z", "event_type": "dns_query", "severity": 2, "message": "q1"},
        {"timestamp": "2026-02-14T18:23:42Z", "event_type": "dns_query", "severity": 2, "message": "q2"},
    ]
    r = client.post("/api/v1/ingest/batch", json=batch)
    assert r.status_code == 200
    assert r.json()["inserted"] == 2

    q = client.get("/api/v1/events?event_type=dns_query&limit=10")
    assert q.status_code == 200
    assert q.json()["total"] == 2
