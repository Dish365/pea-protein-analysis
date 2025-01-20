// Define base API URL
export const API_BASE_URL =
  process.env.REACT_APP_API_URL || "http://localhost:8000";

// Define API endpoints
export const ENDPOINTS = {
  // Auth endpoints
  AUTH: {
    LOGIN: `${API_BASE_URL}/auth/login`,
    REGISTER: `${API_BASE_URL}/auth/register`,
    LOGOUT: `${API_BASE_URL}/auth/logout`,
  },

  // User endpoints
  USER: {
    PROFILE: `${API_BASE_URL}/user/profile`,
    UPDATE: `${API_BASE_URL}/user/update`,
  },

  // API endpoints
  API: {
    BASE: API_BASE_URL,
  },
};

export default ENDPOINTS;
