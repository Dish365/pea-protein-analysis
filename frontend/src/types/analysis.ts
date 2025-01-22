import { ProcessAnalysis } from './process';

export interface ProteinRecovery {
  mass: number;
  content: number;
  yield: number;
}

export interface ParticleSizeDistribution {
  d10: number;
  d50: number;
  d90: number;
}

export interface TechnicalResults {
  protein_recovery: ProteinRecovery;
  separation_efficiency: number;
  process_efficiency: number;
  particle_size_distribution: ParticleSizeDistribution;
}

export interface CapexAnalysis {
  total_capex: number;
  equipment_cost: number;
  installation_cost: number;
  indirect_cost: number;
}

export interface OpexAnalysis {
  total_opex: number;
  utilities_cost: number;
  materials_cost: number;
  labor_cost: number;
  maintenance_cost: number;
}

export interface ProfitabilityAnalysis {
  npv: number;
  roi: number;
  payback_period?: number;
  profitability_index?: number;
}

export interface EconomicResults {
  capex_analysis: CapexAnalysis;
  opex_analysis: OpexAnalysis;
  profitability_analysis: ProfitabilityAnalysis;
}

export interface ImpactAssessment {
  gwp: number;
  hct: number;
  frs: number;
}

export interface ConsumptionMetrics {
  electricity: number | null;
  cooling: number | null;
  water: number | null;
}

export interface EnvironmentalResults {
  impact_assessment: ImpactAssessment;
  consumption_metrics: ConsumptionMetrics;
}

export interface EfficiencyMetrics {
  eco_efficiency_index: number;
}

export interface PerformanceIndicators {
  relative_performance: number;
}

export interface EfficiencyResults {
  efficiency_metrics: EfficiencyMetrics;
  performance_indicators: PerformanceIndicators;
}

export interface AnalysisSummary {
  technical: TechnicalResults;
  economic: EconomicResults;
  environmental: EnvironmentalResults;
  efficiency: EfficiencyResults;
}

export interface AnalysisResult {
  id: number;
  process: ProcessAnalysis;
  timestamp: string;
  technical_results: TechnicalResults;
  economic_results: EconomicResults;
  environmental_results: EnvironmentalResults;
  efficiency_results: EfficiencyResults;
  summary?: AnalysisSummary;
  status: 'success' | 'failed';
  message?: string;
}

export interface AnalysisRequest {
  type: string;
  parameters: Record<string, any>;
  datasetId: string;
}

export interface AnalysisFilter {
  startDate?: string;
  endDate?: string;
  status?: string;
  type?: string;
}

export type AnalysisType = "statistical" | "predictive" | "diagnostic";

export interface AnalysisMetadata {
  name: string;
  description: string;
  type: AnalysisType;
  requiredParameters: string[];
}
