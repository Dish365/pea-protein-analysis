import axios from "axios";
import { API_BASE_URL, API_CONFIG, API_ENDPOINTS } from "@/config/api";

// Create axios instance with default configuration
const api = axios.create({
  baseURL: API_BASE_URL,
  ...API_CONFIG,
});

// Add auth interceptor
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Add refresh token interceptor
api.interceptors.response.use(
  (response) => {
    // Ensure response data is serializable
    if (response.data) {
      response.data = JSON.parse(JSON.stringify(response.data));
    }
    return response;
  },
  async (error) => {
    const originalRequest = error.config;

    // Handle 401 Unauthorized errors with token refresh
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const refresh = localStorage.getItem("refreshToken");
        const response = await axios.post(
          API_ENDPOINTS.auth.refresh,
          { refresh }
        );

        const newToken = response.data.access;
        localStorage.setItem("token", newToken);
        originalRequest.headers.Authorization = `Bearer ${newToken}`;

        return api(originalRequest);
      } catch (refreshError) {
        // Clear auth state on refresh failure
        localStorage.removeItem("token");
        localStorage.removeItem("refreshToken");
        window.location.href = "/signin";
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

export default api;
