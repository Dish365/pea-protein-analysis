import { ProcessType } from '../types/process';

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
  { value: ProcessType.BASELINE, label: 'Baseline' },
  { value: ProcessType.RF, label: 'RF Treatment' },
  { value: ProcessType.IR, label: 'IR Treatment' },
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
  process_type: ProcessType.BASELINE,
  air_flow: 500.0,
  classifier_speed: 1500.0,
  input_mass: 100.0,
  output_mass: 80.0,
  initial_protein_content: 25.0,
  final_protein_content: 28.0,
  initial_moisture_content: 15.0,
  final_moisture_content: 10.0,
  d10_particle_size: 10.0,
  d50_particle_size: 50.0,
  d90_particle_size: 90.0,
  equipment_cost: 50000.0,
  maintenance_cost: 5000.0,
  raw_material_cost: 2.5,
  utility_cost: 1.5,
  labor_cost: 25.0,
  project_duration: 10,
  discount_rate: 0.1,
  production_volume: 1000.0,
  electricity_consumption: 150.0,
  cooling_consumption: 50.0,
  water_consumption: 200.0,
  transport_consumption: 100.0,
  equipment_mass: 1000.0,
  ...DEFAULT_PROCESS_VALUES,
};
