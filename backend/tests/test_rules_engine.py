from datetime import UTC, datetime

from app.models.enums import LogLevel, Severity
from app.schemas.log_entry import LogEntryIn
from app.services import rules_engine


def _log(service: str, level: LogLevel) -> LogEntryIn:
    return LogEntryIn(
        service_name=service,
        level=level,
        message="something happened",
        event_timestamp=datetime.now(UTC),
    )


def test_low_severity_for_info_logs():
    logs = [_log("api", LogLevel.INFO) for _ in range(3)]
    assert rules_engine.derive_severity(logs) == Severity.LOW


def test_critical_severity_escalates_with_blast_radius():
    logs = [
        _log("api", LogLevel.CRITICAL),
        _log("worker", LogLevel.ERROR),
        _log("db", LogLevel.ERROR),
    ]
    assert rules_engine.derive_severity(logs) == Severity.CRITICAL


def test_affected_services_are_sorted_and_unique():
    logs = [_log("b", LogLevel.INFO), _log("a", LogLevel.INFO), _log("b", LogLevel.INFO)]
    assert rules_engine.affected_services(logs) == ["a", "b"]
