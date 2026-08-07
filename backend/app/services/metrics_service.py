from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.enums import IncidentStatus
from app.models.incident import Incident
from app.models.log_entry import LogEntry
from app.schemas.metrics import MetricsOverview


class MetricsService:
    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    async def overview(self) -> MetricsOverview:
        by_severity = await self._count_by(Incident.severity)
        by_status = await self._count_by(Incident.status)

        total = sum(by_status.values())
        total_logs = await self._db.scalar(select(func.count()).select_from(LogEntry))

        return MetricsOverview(
            total_incidents=total,
            open_incidents=by_status.get(IncidentStatus.OPEN.value, 0),
            resolved_incidents=by_status.get(IncidentStatus.RESOLVED.value, 0),
            incidents_by_severity=by_severity,
            incidents_by_status=by_status,
            total_log_entries=total_logs or 0,
        )

    async def _count_by(self, column) -> dict[str, int]:
        result = await self._db.execute(
            select(column, func.count()).group_by(column)
        )
        return {str(key): count for key, count in result.all()}
