// Environment configuration
export const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8001";
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
  economic: {
    analyze: `${API_V1_URL}/economic/profitability/analyze/comprehensive`,
  },
  environmental: {
    analyze: `${API_V1_URL}/environmental/impact/analyze-process`,
    impactFactors: `${API_V1_URL}/environmental/impact/impact-factors`,
  }
} as const;

// Type exports
export type ApiEndpoints = typeof API_ENDPOINTS;
