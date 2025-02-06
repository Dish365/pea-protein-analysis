import { TechnicalParameters } from './technical';

export enum ProcessStatus {
  PENDING = 'pending',
  PROCESSING = 'processing',
  COMPLETED = 'completed',
  FAILED = 'failed'
}

export enum ProcessType {
  RF = 'rf',
  IR = 'ir',
  BASELINE = 'baseline',
}

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
  type: ProcessType;
  status: ProcessStatus;
  parameters: Record<string, any>;
  results?: Record<string, any>;
}

