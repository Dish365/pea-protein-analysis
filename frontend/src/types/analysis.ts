import { ProcessType } from "./process";
import { TechnicalResults } from "./technical";
import { EconomicAnalysisResult } from "./economic";
import { EnvironmentalAnalysisResult } from "./environmental";

export interface EfficiencyResults {
  efficiency_metrics: {
    eco_efficiency_index: number;
  };
  performance_indicators: {
    relative_performance: number;
  };
}

export interface AnalysisSummary {
  technical: TechnicalResults;
  economic: EconomicAnalysisResult;
  environmental: EnvironmentalAnalysisResult;
  efficiency: EfficiencyResults;
}

export interface AnalysisResult {
  id: number;
  process: number;
  timestamp: string;
  technical_results: TechnicalResults;
  economic_results: EconomicAnalysisResult;
  environmental_results: EnvironmentalAnalysisResult;
  efficiency_results: EfficiencyResults;
}

export interface AnalysisRequest {
  process_type: ProcessType;
  parameters: Record<string, any>;
}

export interface AnalysisFilter {
  startDate?: string;
  endDate?: string;
  status?: string;
  type?: string;
}

export interface TechnicalParameters {
  processType: "baseline" | "rf" | "ir";
  airFlowRate: number;
  temperature: number;
  pressure: number;
  inputMass: number;
  outputMass: number;
  initialProteinContent: number;
  targetProteinContent: number;
}

export interface EconomicParameters {
  // Add economic parameters
}

export interface EnvironmentalParameters {
  // Add environmental parameters
}
