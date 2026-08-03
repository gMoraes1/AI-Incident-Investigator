import uuid
from datetime import datetime

from pydantic import BaseModel, Field

from app.models.enums import LogLevel


class LogEntryIn(BaseModel):
    service_name: str = Field(min_length=1, max_length=255)
    level: LogLevel = LogLevel.INFO
    message: str = Field(min_length=1)
    trace_id: str | None = None
    event_timestamp: datetime
    context: dict = Field(default_factory=dict)


class LogBatchIn(BaseModel):
    logs: list[LogEntryIn] = Field(min_length=1, max_length=1000)


class LogIngestResult(BaseModel):
    received: int
    stored: int


class LogEntryRead(BaseModel):
    id: uuid.UUID
    service_name: str
    level: LogLevel
    message: str
    fingerprint: str
    trace_id: str | None
    event_timestamp: datetime
    context: dict

    model_config = {"from_attributes": True}
