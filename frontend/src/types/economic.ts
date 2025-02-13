import { ProcessType, ProcessTypeValues } from './process';

export interface CostBreakdown {
  equipment_cost: number;
  utilities_cost: number;
  raw_materials_cost: number;
  labor_cost: number;
  maintenance_cost: number;
  indirect_cost: number;
}

export interface EconomicParameters {
  production_volume: number;
  operating_hours: number;
  
  // Equipment and Costs
  equipment_cost: number;
  installation_factor: number;
  indirect_costs_factor: number;
  maintenance_factor: number;
  
  // Operating Costs
  utility_cost: number;
  raw_material_cost: number;
  labor_cost: number;
  
  // Financial Parameters
  project_duration: number;
  discount_rate: number;
  revenue_per_year: number;
}

export interface EconomicResults {
  capex_analysis: {
    total_capex: number;
    equipment_cost: number;
    installation_cost: number;
    indirect_cost: number;
  };
  opex_analysis: {
    total_opex: number;
    utilities_cost: number;
    materials_cost: number;
    labor_cost: number;
    maintenance_cost: number;
  };
  profitability_analysis: {
    npv: number;
    roi: number;
    payback_period: number;
    irr: number;
  };
  cost_breakdown: CostBreakdown;
  unit_production_cost: number;
}

export interface EconomicAnalysis {
  parameters: EconomicParameters;
  results?: EconomicResults;
} 