import logging

from app.schemas.ai_analysis import AIAnalysisResult
from app.schemas.log_entry import LogEntryIn
from app.services import rules_engine
from app.services.llm.ollama_client import LLMError, OllamaClient
from app.services.llm.prompts import SYSTEM_PROMPT, build_user_prompt

logger = logging.getLogger(__name__)

_MAX_DIGEST_LINES = 100


def _build_digest(logs: list[LogEntryIn]) -> str:
    lines = [
        f"[{log.event_timestamp.isoformat()}] {log.service_name} "
        f"{log.level.upper()}: {log.message}"
        for log in logs[:_MAX_DIGEST_LINES]
    ]
    return "\n".join(lines)


def _fallback(logs: list[LogEntryIn]) -> AIAnalysisResult:
    """Deterministic analysis when the LLM is unavailable."""
    return AIAnalysisResult(
        root_cause="Automatic heuristic analysis (LLM unavailable).",
        severity=rules_engine.derive_severity(logs),
        recommendations=[
            "Inspect the most frequent error signature.",
            "Check recent deployments of the affected services.",
        ],
        affected_services=rules_engine.affected_services(logs),
        confidence=0.3,
    )


class AIAnalysisService:
    def __init__(self, llm: OllamaClient | None = None) -> None:
        self._llm = llm or OllamaClient()

    async def analyze(self, logs: list[LogEntryIn]) -> tuple[AIAnalysisResult, str]:
        """Return the analysis and the model name that produced it."""
        baseline = rules_engine.derive_severity(logs)
        user_prompt = build_user_prompt(_build_digest(logs), baseline.value)

        try:
            raw = await self._llm.generate_json(SYSTEM_PROMPT, user_prompt)
            result = AIAnalysisResult.model_validate(raw)
            return result, self._llm.model_name
        except (LLMError, ValueError) as exc:
            logger.warning("Falling back to rules engine: %s", exc)
            return _fallback(logs), "rules-engine-fallback"
