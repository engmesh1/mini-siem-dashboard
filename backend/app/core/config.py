from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]  # backend/

@dataclass(frozen=True)
class Settings:
    app_name: str = "Mini SIEM Dashboard"
    api_prefix: str = "/api/v1"
    db_path: Path = Path(os.getenv("SIEM_DB_PATH", str(BASE_DIR / "data" / "siem.db")))

settings = Settings()
