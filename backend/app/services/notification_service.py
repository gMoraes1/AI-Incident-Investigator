import logging

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.enums import NotificationChannel, NotificationStatus, Severity
from app.models.incident import Incident
from app.models.notification import Notification

logger = logging.getLogger(__name__)

# Only page humans for incidents at or above this severity.
_NOTIFY_THRESHOLD = {Severity.HIGH, Severity.CRITICAL}


class NotificationService:
    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    async def notify_incident(self, incident: Incident) -> Notification | None:
        if incident.severity not in _NOTIFY_THRESHOLD:
            return None

        notification = Notification(
            channel=NotificationChannel.WEBHOOK,
            target="default-oncall",
            payload=f"[{incident.severity.upper()}] {incident.title}",
            status=NotificationStatus.PENDING,
            incident_id=incident.id,
        )
        self._db.add(notification)

        # Real delivery (Slack/webhook) is wired in V2; here we mark as sent.
        try:
            await self._dispatch(notification)
            notification.status = NotificationStatus.SENT
        except Exception as exc:  # noqa: BLE001 - persisted for observability
            notification.status = NotificationStatus.FAILED
            notification.error = str(exc)
            logger.exception("Failed to dispatch notification")

        await self._db.flush()
        return notification

    async def _dispatch(self, notification: Notification) -> None:
        logger.info("Dispatching notification: %s", notification.payload)
