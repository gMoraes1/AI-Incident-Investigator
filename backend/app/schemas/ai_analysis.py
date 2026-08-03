import uuid

from pydantic import BaseModel, Field

from app.models.enums import Severity


class AIAnalysisResult(BaseModel):
    """Structured output expected from the LLM."""

    root_cause: str
    severity: Severity
    recommendations: list[str] = Field(default_factory=list)
    affected_services: list[str] = Field(default_factory=list)
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)


class AIAnalysisRead(BaseModel):
    id: uuid.UUID
    root_cause: str
    recommendations: list[str]
    affected_services: list[str]
    confidence: float
    model_name: str

    model_config = {"from_attributes": True}
