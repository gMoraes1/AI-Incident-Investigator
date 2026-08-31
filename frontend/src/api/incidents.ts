import type {
  IncidentDetail,
  IncidentStatus,
  LogEntryInput,
  PaginatedIncidents,
} from '@/types';

import { apiClient } from './client';

export interface ListIncidentsParams {
  status?: IncidentStatus;
  limit?: number;
  offset?: number;
}

export async function listIncidents(
  params: ListIncidentsParams = {},
): Promise<PaginatedIncidents> {
  const { data } = await apiClient.get<PaginatedIncidents>('/incidents', { params });
  return data;
}

export async function getIncident(id: string): Promise<IncidentDetail> {
  const { data } = await apiClient.get<IncidentDetail>(`/incidents/${id}`);
  return data;
}

export async function analyzeIncident(
  logs: LogEntryInput[],
  title?: string,
): Promise<IncidentDetail> {
  const { data } = await apiClient.post<IncidentDetail>('/incidents/analyze', {
    title: title ?? null,
    logs,
  });
  return data;
}

export async function updateIncidentStatus(
  id: string,
  status: IncidentStatus,
): Promise<void> {
  await apiClient.patch(`/incidents/${id}/status`, { status });
}
