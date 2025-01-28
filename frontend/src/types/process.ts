import { TechnicalParameters } from './technical';

export enum ProcessType {
  BASELINE = 'baseline',
  RF = 'rf',
  IR = 'ir'
}

export type ProcessStatus = 'pending' | 'processing' | 'completed' | 'failed';

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

export interface ProcessAnalysis extends 
  TechnicalParameters,
  ResourceConfiguration,
  AllocationConfiguration,
  RiskConfiguration {
  
  // Basic Info
  id: number;
  process_type: ProcessType;
  timestamp: string;
  status: ProcessStatus;
  progress: number;

  // Equipment and Costs
  equipment_cost: number;
  maintenance_cost: number;
  installation_factor: number;
  indirect_costs_factor: number;
  maintenance_factor: number;

  // Operating Costs
  raw_material_cost: number;
  utility_cost: number;
  labor_cost: number;

  // Financial Parameters
  project_duration: number;
  discount_rate: number;
  production_volume: number;
  revenue_per_year: number;
  cash_flows: number[];

  // Environmental Analysis
  electricity_consumption: number;
  cooling_consumption: number;
  water_consumption: number;
  transport_consumption: number;
  equipment_mass: number;
  thermal_ratio: number;

  // Production Data
  energy_consumption: Record<string, number>;
  production_data: Record<string, any>;
  product_values: Record<string, number>;
}

