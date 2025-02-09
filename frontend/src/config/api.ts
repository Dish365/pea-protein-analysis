export const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export const API_ENDPOINTS = {
  // Auth endpoints
  auth: {
    signIn: "/api/v1/auth/token/",
    signUp: "/api/v1/auth/register/",
    refreshToken: "/api/v1/auth/token/refresh/",
    resetPassword: "/api/v1/auth/reset-password/",
  },

  // Process analysis endpoints
  process: {
    submit: "/api/v1/process/",
    getById: (id: string) => `/api/v1/process/${id}/`,
    getResults: (id: string) => `/api/v1/process/${id}/results/`,
    getStatus: (id: string) => `/api/v1/process/${id}/status/`,
  },
};
