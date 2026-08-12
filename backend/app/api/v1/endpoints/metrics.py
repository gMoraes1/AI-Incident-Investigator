from fastapi import APIRouter

from app.api.deps import CurrentUser, DbSession
from app.schemas.metrics import MetricsOverview
from app.services.metrics_service import MetricsService

router = APIRouter(prefix="/metrics", tags=["metrics"])


@router.get("", response_model=MetricsOverview)
async def get_metrics(db: DbSession, _: CurrentUser) -> MetricsOverview:
    return await MetricsService(db).overview()
