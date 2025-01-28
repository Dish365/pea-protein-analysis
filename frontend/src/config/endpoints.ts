import { ProcessType } from '../types/process';

// Base URLs
export const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || "http://localhost:8000";
export const API_V1_URL = `${API_BASE_URL}/api/v1`;

// Process Analysis Endpoints
export const PROCESS_ENDPOINTS = {
  BASE: `${API_V1_URL}/process`,
  LIST: `${API_V1_URL}/process/`,
  CREATE: `${API_V1_URL}/process/`,
  DETAIL: (id: number) => `${API_V1_URL}/process/${id}/`,
  STATUS: (id: number) => `${API_V1_URL}/process/${id}/status/`,
  RESULTS: (id: number) => `${API_V1_URL}/process/${id}/results/`,
} as const;

// Request configs
export const API_CONFIG = {
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000, // 30 seconds
} as const;

export type ProcessEndpoint = typeof PROCESS_ENDPOINTS;
