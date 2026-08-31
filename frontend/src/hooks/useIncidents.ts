import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';

import {
  analyzeIncident,
  getIncident,
  listIncidents,
  updateIncidentStatus,
  type ListIncidentsParams,
} from '@/api/incidents';
import { getMetrics } from '@/api/metrics';
import type { IncidentStatus, LogEntryInput } from '@/types';

export function useIncidents(params: ListIncidentsParams = {}) {
  return useQuery({
    queryKey: ['incidents', params],
    queryFn: () => listIncidents(params),
  });
}

export function useIncident(id: string) {
  return useQuery({
    queryKey: ['incident', id],
    queryFn: () => getIncident(id),
    enabled: Boolean(id),
  });
}

export function useMetrics() {
  return useQuery({ queryKey: ['metrics'], queryFn: getMetrics });
}

export function useAnalyzeIncident() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ logs, title }: { logs: LogEntryInput[]; title?: string }) =>
      analyzeIncident(logs, title),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['incidents'] });
      queryClient.invalidateQueries({ queryKey: ['metrics'] });
    },
  });
}

export function useUpdateIncidentStatus() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ id, status }: { id: string; status: IncidentStatus }) =>
      updateIncidentStatus(id, status),
    onSuccess: (_data, variables) => {
      queryClient.invalidateQueries({ queryKey: ['incident', variables.id] });
      queryClient.invalidateQueries({ queryKey: ['incidents'] });
    },
  });
}
