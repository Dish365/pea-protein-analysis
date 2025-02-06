import { ProcessType } from '@/types/process';

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
  DASHBOARD: "/dashboard",
};

export const PROCESS_TYPES = [
  {
    value: ProcessType.BASELINE,
    label: 'Baseline Process',
  },
  {
    value: ProcessType.RF,
    label: 'RF Process',
  },
  {
    value: ProcessType.IR,
    label: 'IR Process',
  },
];

export const ALLOCATION_METHODS = [
  { value: 'economic', label: 'Economic' },
  { value: 'physical', label: 'Physical' },
  { value: 'hybrid', label: 'Hybrid' },
];

export const DEFAULT_HYBRID_WEIGHTS = {
  physical: 0.5,
  economic: 0.5,
};

export const DEFAULT_PROCESS_VALUES = {
  // Process factors
  installation_factor: 0.2,
  indirect_costs_factor: 0.15,
  maintenance_factor: 0.05,
  thermal_ratio: 0.3,
  sensitivity_range: 0.2,
  steps: 10,
};

export const PROCESS_STATUS_LABELS = {
  pending: 'Pending',
  processing: 'Processing',
  completed: 'Completed',
  failed: 'Failed',
};

export const PROCESS_STATUS_COLORS = {
  pending: 'warning',
  processing: 'info',
  completed: 'success',
  failed: 'error',
};

// Default values for new process analysis
export const DEFAULT_PROCESS_ANALYSIS = {
  processType: ProcessType.BASELINE,
  airFlowRate: 500,
  temperature: 25,
  pressure: 1,
  inputMass: 100,
  outputMass: 80,
  initialProteinContent: 25,
  targetProteinContent: 28,
};
