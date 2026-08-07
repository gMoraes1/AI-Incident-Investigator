import uuid

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.ai_analysis import AIAnalysis
from app.models.enums import IncidentStatus
from app.models.incident import Incident
from app.schemas.incident import IncidentAnalyzeRequest
from app.services import rules_engine
from app.services.ai_analysis_service import AIAnalysisService
from app.services.log_service import LogService
from app.services.notification_service import NotificationService


class IncidentNotFoundError(Exception):
    pass


class IncidentService:
    def __init__(
        self,
        db: AsyncSession,
        ai_service: AIAnalysisService | None = None,
    ) -> None:
        self._db = db
        self._logs = LogService(db)
        self._ai = ai_service or AIAnalysisService()
        self._notifications = NotificationService(db)

    async def analyze_and_create(
        self, request: IncidentAnalyzeRequest, created_by_id: uuid.UUID | None
    ) -> Incident:
        """Full investigation pipeline: correlate -> AI -> persist -> notify."""
        logs = request.logs
        analysis_result, model_name = await self._ai.analyze(logs)

        title = request.title or self._infer_title(logs)
        incident = Incident(
            title=title,
            summary=analysis_result.root_cause,
            severity=analysis_result.severity,
            status=IncidentStatus.OPEN,
            fingerprint=rules_engine.dominant_fingerprint(logs),
            created_by_id=created_by_id,
        )
        incident.analysis = AIAnalysis(
            root_cause=analysis_result.root_cause,
            recommendations=analysis_result.recommendations,
            affected_services=analysis_result.affected_services,
            confidence=analysis_result.confidence,
            model_name=model_name,
        )
        incident.log_entries = [
            self._logs._to_model(log) for log in logs
        ]

        self._db.add(incident)
        await self._db.flush()

        await self._notifications.notify_incident(incident)
        await self._db.refresh(incident)
        return await self.get(incident.id)

    async def get(self, incident_id: uuid.UUID) -> Incident:
        result = await self._db.execute(
            select(Incident)
            .where(Incident.id == incident_id)
            .options(
                selectinload(Incident.analysis),
                selectinload(Incident.log_entries),
            )
        )
        incident = result.scalar_one_or_none()
        if incident is None:
            raise IncidentNotFoundError(str(incident_id))
        return incident

    async def list(
        self,
        *,
        status: IncidentStatus | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> tuple[int, list[Incident]]:
        base = select(Incident)
        if status is not None:
            base = base.where(Incident.status == status)

        total = await self._db.scalar(
            select(func.count()).select_from(base.subquery())
        )
        result = await self._db.execute(
            base.order_by(Incident.created_at.desc()).limit(limit).offset(offset)
        )
        return total or 0, list(result.scalars().all())

    async def update_status(
        self, incident_id: uuid.UUID, status: IncidentStatus
    ) -> Incident:
        incident = await self.get(incident_id)
        incident.status = status
        await self._db.flush()
        return incident

    @staticmethod
    def _infer_title(logs) -> str:
        services = rules_engine.affected_services(logs)
        scope = ", ".join(services[:3]) or "unknown service"
        return f"Incident detected in {scope}"
