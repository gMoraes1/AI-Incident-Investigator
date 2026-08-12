import uuid

from fastapi import APIRouter, HTTPException, Query, status

from app.api.deps import CurrentUser, DbSession
from app.models.enums import IncidentStatus
from app.schemas.incident import (
    IncidentAnalyzeRequest,
    IncidentDetail,
    IncidentRead,
    IncidentStatusUpdate,
    PaginatedIncidents,
)
from app.services.incident_service import IncidentNotFoundError, IncidentService

router = APIRouter(prefix="/incidents", tags=["incidents"])


@router.post("/analyze", response_model=IncidentDetail, status_code=status.HTTP_201_CREATED)
async def analyze_incident(
    request: IncidentAnalyzeRequest,
    db: DbSession,
    current_user: CurrentUser,
) -> IncidentDetail:
    incident = await IncidentService(db).analyze_and_create(request, current_user.id)
    return IncidentDetail.model_validate(incident)


@router.get("", response_model=PaginatedIncidents)
async def list_incidents(
    db: DbSession,
    _: CurrentUser,
    status_filter: IncidentStatus | None = Query(default=None, alias="status"),
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
) -> PaginatedIncidents:
    total, incidents = await IncidentService(db).list(
        status=status_filter, limit=limit, offset=offset
    )
    return PaginatedIncidents(
        total=total, items=[IncidentRead.model_validate(i) for i in incidents]
    )


@router.get("/{incident_id}", response_model=IncidentDetail)
async def get_incident(
    incident_id: uuid.UUID,
    db: DbSession,
    _: CurrentUser,
) -> IncidentDetail:
    try:
        incident = await IncidentService(db).get(incident_id)
    except IncidentNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Incident not found"
        ) from exc
    return IncidentDetail.model_validate(incident)


@router.patch("/{incident_id}/status", response_model=IncidentRead)
async def update_incident_status(
    incident_id: uuid.UUID,
    update: IncidentStatusUpdate,
    db: DbSession,
    _: CurrentUser,
) -> IncidentRead:
    try:
        incident = await IncidentService(db).update_status(incident_id, update.status)
    except IncidentNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Incident not found"
        ) from exc
    return IncidentRead.model_validate(incident)
