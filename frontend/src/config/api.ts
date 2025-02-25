// Environment configuration
export const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "/api";  // Ensure we always have /api prefix
export const API_V1_URL = `${API_BASE_URL}/v1`;

// API Configuration
export const API_CONFIG = {
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000, // 30 seconds
} as const;

// API Endpoints
export const API_ENDPOINTS = {
  protein: {
    completeAnalysis: `${API_V1_URL}/protein/protein-analysis/complete-analysis/`,
    recovery: `${API_V1_URL}/protein/protein-analysis/recovery/`,
    separation: `${API_V1_URL}/protein/protein-analysis/separation/`,
    particleSize: `${API_V1_URL}/protein/protein-analysis/particle-size/`,
  },
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
