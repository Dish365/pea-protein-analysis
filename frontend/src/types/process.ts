import { TechnicalParameters } from './technical';

export enum ProcessStatus {
  PENDING = 'pending',
  PROCESSING = 'processing',
  COMPLETED = 'completed',
  FAILED = 'failed'
}

export enum ProcessType {
  BASELINE = 'baseline',
  RF = 'rf',
  IR = 'ir'
}

export type ProcessTypeValues = 'baseline' | 'rf' | 'ir';

export interface Equipment {
  name: string;
  cost: number;
  efficiency: number;
  maintenance_cost: number;
  energy_consumption: number;
  processing_capacity: number;
}

export interface Utility {
  name: string;
  consumption: number;
  unit_price: number;
  unit: string;
}

export interface RawMaterial {
  name: string;
  quantity: number;
  unit_price: number;
  unit: string;
}

export interface LaborConfig {
  hourly_wage: number;
  hours_per_week: number;
  weeks_per_year: number;
  num_workers: number;
}

export interface IndirectFactor {
  name: string;
  cost: number;
  percentage: number;
}

export interface ResourceConfiguration {
  equipment: Equipment[];
  utilities: Utility[];
  raw_materials: RawMaterial[];
  labor_config: LaborConfig;
  indirect_factors: IndirectFactor[];
}

export interface AllocationConfiguration {
  allocation_method: 'economic' | 'physical' | 'hybrid';
  hybrid_weights: Record<string, number>;
}

export interface RiskConfiguration {
  sensitivity_range: number;
  steps: number;
}

export interface ProcessAnalysis {
  id: string;
  process_type: ProcessType;
  timestamp: string;
  status: ProcessStatus;
  progress: number;
  
  // Technical Analysis Inputs
  air_flow: number;
  classifier_speed: number;
  input_mass: number;
  output_mass: number;
  initial_protein_content: number;
  final_protein_content: number;
  initial_moisture_content: number;
  final_moisture_content: number;
  d10_particle_size: number;
  d50_particle_size: number;
  d90_particle_size: number;
  
  // Economic Analysis Inputs
  equipment: Equipment[];
  equipment_cost: number;
  maintenance_cost: number;
  installation_factor: number;
  indirect_costs_factor: number;
  maintenance_factor: number;
  indirect_factors: IndirectFactor[];
  raw_material_cost: number;
  utility_cost: number;
  labor_cost: number;
  utilities: Utility[];
  raw_materials: RawMaterial[];
  labor_config: LaborConfig;
  project_duration: number;
  discount_rate: number;
  production_volume: number;
  revenue_per_year: number;
  cash_flows: number[];
  
  // Risk Analysis
  sensitivity_range: number;
  steps: number;
  
  // Environmental Analysis Inputs
  electricity_consumption: number;
  cooling_consumption: number;
  water_consumption: number;
  transport_consumption: number;
  equipment_mass: number;
  thermal_ratio: number;
  energy_consumption: Record<string, number>;
  production_data: Record<string, any>;
  product_values: Record<string, any>;
  
  // Allocation Configuration
  allocation_method: 'economic' | 'physical' | 'hybrid';
  hybrid_weights: Record<string, number>;
  
  // Results
  technical_results?: Record<string, any>;
  economic_results?: Record<string, any>;
  environmental_results?: Record<string, any>;
  efficiency_results?: Record<string, any>;
}

