import hashlib
import re

# Patterns of volatile tokens that must be masked so that structurally
# identical messages collapse to the same fingerprint.
_UUID_RE = r"\b[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}\b"

_PATTERNS: list[tuple[re.Pattern[str], str]] = [
    (re.compile(_UUID_RE), "<uuid>"),
    (re.compile(r"\b\d{1,3}(?:\.\d{1,3}){3}\b"), "<ip>"),
    (re.compile(r"\b[\w.+-]+@[\w-]+\.[\w.-]+\b"), "<email>"),
    (re.compile(r"0x[0-9a-fA-F]+"), "<hex>"),
    (re.compile(r"\b\d+\b"), "<num>"),
]


def normalize_message(message: str) -> str:
    normalized = message.strip().lower()
    for pattern, replacement in _PATTERNS:
        normalized = pattern.sub(replacement, normalized)
    return re.sub(r"\s+", " ", normalized).strip()


def fingerprint(service_name: str, message: str) -> str:
    """Stable hash grouping structurally-similar events of a service."""
    normalized = normalize_message(message)
    digest = hashlib.sha1(f"{service_name}:{normalized}".encode()).hexdigest()
    return digest[:32]
