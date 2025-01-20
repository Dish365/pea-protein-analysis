// API and Environment Constants
export const API_BASE_URL =
  process.env.REACT_APP_API_BASE_URL || "http://localhost:8000";

// Authentication Constants
export const TOKEN_KEY = "auth_token";
export const REFRESH_TOKEN_KEY = "refresh_token";

// Application Constants
export const APP_NAME = "Your App Name";
export const DEFAULT_LANGUAGE = "en";

// Pagination Constants
export const DEFAULT_PAGE_SIZE = 10;
export const DEFAULT_PAGE_NUMBER = 1;

// Time Constants
export const TOKEN_EXPIRY_TIME = 3600; // in seconds
export const REFRESH_TOKEN_EXPIRY_TIME = 86400; // in seconds

// Route Constants
export const ROUTES = {
  HOME: "/",
  LOGIN: "/login",
  REGISTER: "/register",
  DASHBOARD: "/dashboard",
  PROFILE: "/profile",
};
