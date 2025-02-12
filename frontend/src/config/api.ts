// Environment configuration
export const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
export const API_V1_URL = `${API_BASE_URL}/api/v1`;

// API Configuration
export const API_CONFIG = {
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000, // 30 seconds
} as const;

// API Endpoints
export const API_ENDPOINTS = {
  auth: {
    token: `${API_V1_URL}/auth/token/`,
    refresh: `${API_V1_URL}/auth/token/refresh/`,
    register: `${API_V1_URL}/auth/register/`,
    resetPassword: `${API_V1_URL}/auth/reset-password/`,
  },
  
  process: {
    base: `${API_V1_URL}/process`,
    list: `${API_V1_URL}/process/`,
    create: `${API_V1_URL}/process/`,
    detail: (id: string) => `${API_V1_URL}/process/${id}/`,
    status: (id: string) => `${API_V1_URL}/process/${id}/status/`,
    results: (id: string) => `${API_V1_URL}/process/${id}/results/`,
  },
  analysis: {
    create: `${API_V1_URL}/process/analysis/create/`,
    update: (id: string) => `${API_V1_URL}/process/analysis/${id}/update/`,
    submit: (id: string) => `${API_V1_URL}/process/analysis/${id}/submit/`,
    technical: (id: string) => `${API_V1_URL}/process/analysis/${id}/technical/`,
    economic: (id: string) => `${API_V1_URL}/process/analysis/${id}/economic/`,
    environmental: (id: string) => `${API_V1_URL}/process/analysis/${id}/environmental/`,
  }
} as const;

// Type exports
export type ApiEndpoints = typeof API_ENDPOINTS;
export type ProcessEndpoints = typeof API_ENDPOINTS.process;
