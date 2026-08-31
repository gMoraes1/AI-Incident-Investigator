import type { User } from '@/types';

import { apiClient } from './client';

export async function login(email: string, password: string): Promise<string> {
  // The backend login endpoint expects OAuth2 form-encoded credentials.
  const form = new URLSearchParams({ username: email, password });
  const { data } = await apiClient.post<{ access_token: string }>('/auth/login', form, {
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
  });
  return data.access_token;
}

export async function register(
  email: string,
  password: string,
  fullName?: string,
): Promise<User> {
  const { data } = await apiClient.post<User>('/auth/register', {
    email,
    password,
    full_name: fullName ?? null,
  });
  return data;
}

export async function fetchMe(): Promise<User> {
  const { data } = await apiClient.get<User>('/auth/me');
  return data;
}
