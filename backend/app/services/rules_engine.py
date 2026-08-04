from collections import Counter

from app.models.enums import LogLevel, Severity
from app.schemas.log_entry import LogEntryIn

# Weight given to each log level when scoring a group of events.
_LEVEL_WEIGHTS: dict[LogLevel, int] = {
    LogLevel.DEBUG: 0,
    LogLevel.INFO: 0,
    LogLevel.WARNING: 1,
    LogLevel.ERROR: 3,
    LogLevel.CRITICAL: 5,
}


def derive_severity(logs: list[LogEntryIn]) -> Severity:
    """Heuristic severity used as a baseline before the LLM refines it."""
    if not logs:
        return Severity.LOW

    score = sum(_LEVEL_WEIGHTS.get(log.level, 0) for log in logs)
    affected_services = len({log.service_name for log in logs})
    # Multi-service blast radius escalates severity.
    score += (affected_services - 1) * 2

    if score >= 12:
        return Severity.CRITICAL
    if score >= 6:
        return Severity.HIGH
    if score >= 2:
        return Severity.MEDIUM
    return Severity.LOW


def dominant_fingerprint(logs: list[LogEntryIn]) -> str | None:
    from app.services.normalizer import fingerprint

    if not logs:
        return None
    counts = Counter(fingerprint(log.service_name, log.message) for log in logs)
    return counts.most_common(1)[0][0]


def affected_services(logs: list[LogEntryIn]) -> list[str]:
    return sorted({log.service_name for log in logs})
