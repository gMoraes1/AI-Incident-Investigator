from fastapi import APIRouter, status

from app.api.deps import CurrentUser, DbSession
from app.schemas.log_entry import LogBatchIn, LogIngestResult
from app.services.log_service import LogService

router = APIRouter(prefix="/logs", tags=["logs"])


@router.post("", response_model=LogIngestResult, status_code=status.HTTP_202_ACCEPTED)
async def ingest_logs(
    batch: LogBatchIn,
    db: DbSession,
    _: CurrentUser,
) -> LogIngestResult:
    stored = await LogService(db).ingest(batch.logs)
    return LogIngestResult(received=len(batch.logs), stored=stored)
