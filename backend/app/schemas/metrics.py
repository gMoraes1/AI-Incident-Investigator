from pydantic import BaseModel


class MetricsOverview(BaseModel):
    total_incidents: int
    open_incidents: int
    resolved_incidents: int
    incidents_by_severity: dict[str, int]
    incidents_by_status: dict[str, int]
    total_log_entries: int
