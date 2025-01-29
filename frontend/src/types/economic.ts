export interface EconomicParameters {
  // Capital Costs
  equipment_cost: number;
  maintenance_cost: number;
  installation_factor: number;
  indirect_costs_factor: number;
  maintenance_factor: number;

  // Operating Costs
  raw_material_cost: number;
  utility_cost: number;
  labor_cost: number;

  // Project Parameters
  project_duration: number;
  discount_rate: number;
  production_volume: number;
  revenue_per_year: number;
}

export interface EconomicAnalysisResult {
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
} 