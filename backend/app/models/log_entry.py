import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import JSON, DateTime, Enum, ForeignKey, String, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.enums import LogLevel
from app.models.mixins import TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.models.incident import Incident


class LogEntry(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "log_entries"

    service_name: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    level: Mapped[LogLevel] = mapped_column(
        Enum(LogLevel, name="log_level"), default=LogLevel.INFO, nullable=False, index=True
    )
    message: Mapped[str] = mapped_column(Text, nullable=False)
    # Fingerprint of the normalized message, used to group similar events.
    fingerprint: Mapped[str] = mapped_column(String(128), index=True, nullable=False)
    trace_id: Mapped[str | None] = mapped_column(String(128), index=True)
    event_timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, index=True
    )
    context: Mapped[dict] = mapped_column(JSON, default=dict)

    incident_id: Mapped[uuid.UUID | None] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("incidents.id", ondelete="CASCADE"), index=True
    )
    incident: Mapped["Incident | None"] = relationship(back_populates="log_entries")
