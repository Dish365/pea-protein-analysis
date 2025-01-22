// Define base API URL
export const API_BASE_URL = "http://localhost:8000/api/v1";

// Define API endpoints
export const ENDPOINTS = {
  PROCESS: {
    LIST: '/process/',
    CREATE: '/process/',
    DETAIL: (id: number) => `/process/${id}/`,
    STATUS: (id: number) => `/process/${id}/status/`,
    RESULTS: (id: number) => `/process/${id}/results/`,
  },
};

// Axios config can be imported from here
export const axiosConfig = {
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
};

export default ENDPOINTS;
