import uuid
from datetime import datetime

from pydantic import BaseModel, Field

from app.models.enums import IncidentStatus, Severity
from app.schemas.ai_analysis import AIAnalysisRead
from app.schemas.log_entry import LogEntryIn, LogEntryRead


class IncidentAnalyzeRequest(BaseModel):
    """Analyze an ad-hoc batch of logs and open an incident from them."""

    title: str | None = Field(default=None, max_length=500)
    logs: list[LogEntryIn] = Field(min_length=1, max_length=1000)


class IncidentRead(BaseModel):
    id: uuid.UUID
    title: str
    summary: str | None
    status: IncidentStatus
    severity: Severity
    fingerprint: str | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class IncidentDetail(IncidentRead):
    analysis: AIAnalysisRead | None = None
    log_entries: list[LogEntryRead] = Field(default_factory=list)


class IncidentStatusUpdate(BaseModel):
    status: IncidentStatus


class PaginatedIncidents(BaseModel):
    total: int
    items: list[IncidentRead]
