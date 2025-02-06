import { ProcessType } from './process';

export interface CostBreakdown {
  equipment: number;
  utilities: number;
  rawMaterials: number;
  labor: number;
  maintenance: number;
  indirect: number;
}

export interface EconomicParameters {
  processType: ProcessType;
  productionVolume: number;
  operatingHours: number;
  equipmentCost: number;
  utilityRate: number;
  rawMaterialCost: number;
  laborRate: number;
  maintenanceFactor: number;
  indirectCostFactor: number;
}

export interface EconomicResults {
  totalCapitalCost: number;
  operatingCost: number;
  costBreakdown: CostBreakdown;
  unitProductionCost: number;
  paybackPeriod: number;
  roi: number;
  npv: number;
}

export interface EconomicAnalysis {
  parameters: EconomicParameters;
  results?: EconomicResults;
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