# Architecture (MVP-1)

**Client** (curl/Postman/UI) -> **FastAPI** -> **SQLite**

Flow:
1. `POST /api/v1/ingest` receives an event JSON.
2. `normalize_event()` maps fields into a consistent schema.
3. DB layer inserts normalized row + stores full raw JSON.
4. `GET /api/v1/events` queries with filters + pagination.
