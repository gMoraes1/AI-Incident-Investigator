from sqlalchemy.ext.asyncio import AsyncSession

from app.models.log_entry import LogEntry
from app.schemas.log_entry import LogEntryIn
from app.services.normalizer import fingerprint


class LogService:
    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    def _to_model(self, log: LogEntryIn, incident_id=None) -> LogEntry:
        return LogEntry(
            service_name=log.service_name,
            level=log.level,
            message=log.message,
            fingerprint=fingerprint(log.service_name, log.message),
            trace_id=log.trace_id,
            event_timestamp=log.event_timestamp,
            context=log.context,
            incident_id=incident_id,
        )

    async def ingest(self, logs: list[LogEntryIn]) -> int:
        """Normalize and persist a batch of raw logs; returns stored count."""
        entries = [self._to_model(log) for log in logs]
        self._db.add_all(entries)
        await self._db.flush()
        return len(entries)
