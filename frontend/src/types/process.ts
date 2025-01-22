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

export interface ProcessAnalysis {
  // Basic Info
  id?: number;
  process_type: ProcessType;
  timestamp?: string;
  status?: ProcessStatus;
  progress?: number;

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
  sensitivity_range: number;
  steps: number;

  // Environmental Analysis
  electricity_consumption: number;
  cooling_consumption: number;
  water_consumption: number;
  transport_consumption: number;
  equipment_mass: number;
  thermal_ratio: number;
  energy_consumption: {
    electricity: number;
    cooling: number;
  };
  production_data: {
    input_mass: number;
    output_mass: number;
    production_volume: number;
  };
  product_values: {
    main_product: number;
    waste_product: number;
  };
  allocation_method: 'economic' | 'physical' | 'hybrid';
  hybrid_weights: {
    physical: number;
    economic: number;
  };
}
