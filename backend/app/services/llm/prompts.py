SYSTEM_PROMPT = """You are an SRE incident analyst. Given normalized application \
logs, identify the most probable root cause, assess severity, list affected \
services and propose concrete corrective actions.

Respond ONLY with a valid JSON object matching this schema:
{
  "root_cause": string,
  "severity": one of ["low", "medium", "high", "critical"],
  "recommendations": array of short action strings,
  "affected_services": array of service names,
  "confidence": number between 0 and 1
}
Do not include any prose outside the JSON object."""


def build_user_prompt(logs_digest: str, baseline_severity: str) -> str:
    return (
        f"Baseline heuristic severity: {baseline_severity}.\n\n"
        f"Correlated log events:\n{logs_digest}\n\n"
        "Analyze these events and return the JSON analysis."
    )
