# Mini SIEM Dashboard (MVP)

A lightweight, SOC-style mini SIEM prototype that ingests logs, normalizes fields, stores events in SQLite, and exposes a clean API for searching and basic reporting.

> Status: MVP-1 (Ingestion + Storage + Search API)

## Features (MVP-1)
- **Ingest** security events via JSON (single event or batch).
- **Normalize** common fields (`timestamp`, `src_ip`, `dest_ip`, `event_type`, `severity`, `message`).
- **Store** events in **SQLite**.
- **Query** events with filters (time range, IP, event type, severity) + pagination.
- **Export** to CSV.

## Tech Stack
- Backend: **FastAPI** + **Uvicorn**
- Database: **SQLite**
- Tooling: **pytest**, **ruff**, **GitHub Actions**

## Prerequisites
- **Python:** 3.11–3.13 (recommended **3.12**).  
  > Python 3.14+ may fail to install `pydantic-core` on macOS due to upstream Rust/PyO3 compatibility.
- **macOS (Apple Silicon) quick install:**
  ```bash
  brew install python@3.12
  ```

## Quickstart

### 1) Create venv + install
```bash
cd backend
python3.12 -m venv .venv  # or: python3.11 -m venv .venv
# macOS/Linux
source .venv/bin/activate
# Windows
# .venv\Scripts\activate

pip install -r requirements.txt
```

### 2) Run API
```bash
uvicorn app.main:app --reload --port 8000
```

Open:
- API Docs (Swagger): http://127.0.0.1:8000/docs

### 3) Initialize DB (optional)
The app auto-creates the SQLite DB at first run.
DB path defaults to `backend/data/siem.db`.

### 4) Ingest sample events
```bash
curl -X POST "http://127.0.0.1:8000/api/v1/ingest/batch" \
  -H "Content-Type: application/json" \
  --data @../sample_data/events.sample.json
```

### 5) Query events
```bash
curl "http://127.0.0.1:8000/api/v1/events?limit=20"
```

### 6) Export CSV
```bash
curl -L "http://127.0.0.1:8000/api/v1/events/export.csv" -o events.csv
```

## Common Commands (Makefile)
From the repo root:

```bash
make setup
make run
make test
make lint
```

## API Overview
- `POST /api/v1/ingest` (single event)
- `POST /api/v1/ingest/batch` (batch ingest)
- `GET /api/v1/events` (search/paginate)
- `GET /api/v1/events/export.csv` (CSV export)
- `GET /healthz`

## Data Model (normalized)
Each event is normalized into:
- `timestamp` (ISO-8601)
- `src_ip`, `dest_ip` (IPv4/IPv6)
- `event_type` (string)
- `severity` (0-10)
- `message` (string)
- `raw` (original payload JSON)

## Roadmap (MVP-2 / MVP-3)
- Rules engine + alert table (brute force, port scan, etc.)
- Dashboard UI (charts + filtering)
- Docker compose + Postgres option
- Auth / RBAC (optional)

## License
MIT. See [LICENSE](LICENSE).

---

**إنشاء، تصميم، وتنفيذ: المهندس مشاري الخليفة**  
**Created, Designed, and Implemented by: Engineer Meshari Al-Khalifah**


---

**Swagger UI includes a bottom-right credit badge.** Open: `http://127.0.0.1:8000/docs`
