import type { IncidentStatus, Severity } from '@/types';

export function SeverityBadge({ severity }: { severity: Severity }) {
  return <span className={`badge badge--severity-${severity}`}>{severity}</span>;
}

export function StatusBadge({ status }: { status: IncidentStatus }) {
  return <span className={`badge badge--status-${status}`}>{status}</span>;
}
