import type { MetricsOverview } from '@/types';

import { apiClient } from './client';

export async function getMetrics(): Promise<MetricsOverview> {
  const { data } = await apiClient.get<MetricsOverview>('/metrics');
  return data;
}
