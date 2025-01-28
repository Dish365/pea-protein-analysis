export interface EconomicAnalysisResult {
  costs: {
    equipment: number;
    maintenance: number;
    rawMaterial: number;
    utilities: number;
    labor: number;
    indirect: number;
  };
  metrics: {
    totalAnnualCost: number;
    unitCost: number;
    annualRevenue: number;
    annualProfit: number;
    roi: number;
    paybackPeriod: number;
    npv: number;
    irr: number;
  };
  sensitivity: {
    parameter: string;
    baseValue: number;
    impact: number;
    sensitivity: 'Low' | 'Medium' | 'High';
  }[];
} 