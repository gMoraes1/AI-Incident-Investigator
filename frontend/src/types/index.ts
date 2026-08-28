export type Severity = 'low' | 'medium' | 'high' | 'critical';
export type IncidentStatus = 'open' | 'investigating' | 'resolved' | 'closed';
export type LogLevel = 'debug' | 'info' | 'warning' | 'error' | 'critical';

export interface User {
  id: string;
  email: string;
  full_name: string | null;
  role: string;
  is_active: boolean;
}

export interface AIAnalysis {
  id: string;
  root_cause: string;
  recommendations: string[];
  affected_services: string[];
  confidence: number;
  model_name: string;
}

export interface LogEntry {
  id: string;
  service_name: string;
  level: LogLevel;
  message: string;
  fingerprint: string;
  trace_id: string | null;
  event_timestamp: string;
  context: Record<string, unknown>;
}

export interface Incident {
  id: string;
  title: string;
  summary: string | null;
  status: IncidentStatus;
  severity: Severity;
  fingerprint: string | null;
  created_at: string;
  updated_at: string;
}

export interface IncidentDetail extends Incident {
  analysis: AIAnalysis | null;
  log_entries: LogEntry[];
}

export interface PaginatedIncidents {
  total: number;
  items: Incident[];
}

export interface MetricsOverview {
  total_incidents: number;
  open_incidents: number;
  resolved_incidents: number;
  incidents_by_severity: Record<string, number>;
  incidents_by_status: Record<string, number>;
  total_log_entries: number;
}

export interface LogEntryInput {
  service_name: string;
  level: LogLevel;
  message: string;
  trace_id?: string | null;
  event_timestamp: string;
  context?: Record<string, unknown>;
}
