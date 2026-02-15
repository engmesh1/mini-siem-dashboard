from __future__ import annotations

from typing import Any, List, Optional

from pydantic import BaseModel, Field

class IngestEvent(BaseModel):
    # Accept flexible input, normalize later.
    timestamp: str = Field(..., description="ISO-8601 timestamp")
    src_ip: Optional[str] = None
    dest_ip: Optional[str] = None
    event_type: str
    severity: Optional[int] = Field(default=None, ge=0, le=10)
    message: Optional[str] = None

    # allow extra payload
    class Config:
        extra = "allow"

class IngestBatch(BaseModel):
    events: List[IngestEvent]

class EventOut(BaseModel):
    id: int
    timestamp: str
    src_ip: Optional[str]
    dest_ip: Optional[str]
    event_type: str
    severity: int
    message: Optional[str]
    raw: dict[str, Any]

class EventsPage(BaseModel):
    total: int
    limit: int
    offset: int
    items: List[EventOut]
