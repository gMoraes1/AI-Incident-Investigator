import uuid
from typing import TYPE_CHECKING

from sqlalchemy import JSON, Float, ForeignKey, String, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.mixins import TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.models.incident import Incident


class AIAnalysis(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "ai_analysis"

    root_cause: Mapped[str] = mapped_column(Text, nullable=False)
    # List of human-readable recommended actions.
    recommendations: Mapped[list] = mapped_column(JSON, default=list)
    affected_services: Mapped[list] = mapped_column(JSON, default=list)
    confidence: Mapped[float] = mapped_column(Float, default=0.0)
    model_name: Mapped[str] = mapped_column(String(128), nullable=False)

    incident_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("incidents.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )
    incident: Mapped["Incident"] = relationship(back_populates="analysis")
