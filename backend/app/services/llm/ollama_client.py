import json
import logging

import httpx

from app.core.config import settings

logger = logging.getLogger(__name__)


class LLMError(RuntimeError):
    """Raised when the LLM backend is unreachable or returns garbage."""


class OllamaClient:
    def __init__(
        self,
        base_url: str | None = None,
        model: str | None = None,
        timeout: int | None = None,
    ) -> None:
        self._base_url = (base_url or settings.ollama_base_url).rstrip("/")
        self._model = model or settings.ollama_model
        self._timeout = timeout or settings.ollama_timeout_seconds

    async def generate_json(self, system_prompt: str, user_prompt: str) -> dict:
        """Call Ollama in JSON mode and return the parsed response object."""
        payload = {
            "model": self._model,
            "system": system_prompt,
            "prompt": user_prompt,
            "format": "json",
            "stream": False,
        }
        try:
            async with httpx.AsyncClient(timeout=self._timeout) as client:
                response = await client.post(f"{self._base_url}/api/generate", json=payload)
                response.raise_for_status()
        except httpx.HTTPError as exc:
            raise LLMError(f"Ollama request failed: {exc}") from exc

        raw = response.json().get("response", "")
        try:
            return json.loads(raw)
        except json.JSONDecodeError as exc:
            logger.warning("LLM returned non-JSON payload: %s", raw[:200])
            raise LLMError("LLM returned malformed JSON") from exc

    @property
    def model_name(self) -> str:
        return self._model
