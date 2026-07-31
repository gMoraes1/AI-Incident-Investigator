import uuid
from typing import TYPE_CHECKING

from sqlalchemy import Enum, ForeignKey, String, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.enums import IncidentStatus, Severity
from app.models.mixins import TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.models.ai_analysis import AIAnalysis
    from app.models.log_entry import LogEntry
    from app.models.notification import Notification


class Incident(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "incidents"

    title: Mapped[str] = mapped_column(String(500), nullable=False)
    summary: Mapped[str | None] = mapped_column(Text)
    status: Mapped[IncidentStatus] = mapped_column(
        Enum(IncidentStatus, name="incident_status"),
        default=IncidentStatus.OPEN,
        nullable=False,
        index=True,
    )
    severity: Mapped[Severity] = mapped_column(
        Enum(Severity, name="incident_severity"),
        default=Severity.MEDIUM,
        nullable=False,
        index=True,
    )
    fingerprint: Mapped[str | None] = mapped_column(String(128), index=True)

    created_by_id: Mapped[uuid.UUID | None] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL")
    )

    log_entries: Mapped[list["LogEntry"]] = relationship(
        back_populates="incident", cascade="all, delete-orphan"
    )
    analysis: Mapped["AIAnalysis | None"] = relationship(
        back_populates="incident",
        cascade="all, delete-orphan",
        uselist=False,
    )
    notifications: Mapped[list["Notification"]] = relationship(
        back_populates="incident", cascade="all, delete-orphan"
    )
