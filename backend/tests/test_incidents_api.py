from datetime import UTC, datetime

import pytest
from httpx import AsyncClient

from app.services.llm.ollama_client import OllamaClient


@pytest.fixture(autouse=True)
def stub_llm(monkeypatch):
    """Keep the analysis pipeline offline and deterministic in tests."""

    async def fake_generate_json(self, system_prompt: str, user_prompt: str) -> dict:
        return {
            "root_cause": "Database connection pool exhausted",
            "severity": "critical",
            "recommendations": ["Increase pool size", "Restart api pods"],
            "affected_services": ["api", "worker"],
            "confidence": 0.82,
        }

    monkeypatch.setattr(OllamaClient, "generate_json", fake_generate_json)


def _payload() -> dict:
    now = datetime.now(UTC).isoformat()
    return {
        "title": "DB outage",
        "logs": [
            {
                "service_name": "api",
                "level": "critical",
                "message": "connection refused to db",
                "event_timestamp": now,
            },
            {
                "service_name": "worker",
                "level": "error",
                "message": "task failed: db unavailable",
                "event_timestamp": now,
            },
        ],
    }


@pytest.mark.asyncio
async def test_analyze_creates_incident(client: AsyncClient):
    # With no Ollama backend reachable, the pipeline falls back to the rules engine.
    response = await client.post("/api/v1/incidents/analyze", json=_payload())
    assert response.status_code == 201

    body = response.json()
    assert body["title"] == "DB outage"
    assert body["analysis"] is not None
    assert len(body["log_entries"]) == 2

    incident_id = body["id"]
    detail = await client.get(f"/api/v1/incidents/{incident_id}")
    assert detail.status_code == 200
    assert detail.json()["id"] == incident_id


@pytest.mark.asyncio
async def test_list_incidents_empty(client: AsyncClient):
    response = await client.get("/api/v1/incidents")
    assert response.status_code == 200
    assert response.json() == {"total": 0, "items": []}
