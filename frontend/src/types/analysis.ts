import { ProcessType } from "./process";
import { TechnicalParameters, TechnicalResults } from "./technical";
import { EconomicParameters, EconomicResults } from "./economic";
import { EnvironmentalParameters, EnvironmentalResults } from "./environmental";

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
  economic: EconomicResults;
  environmental: EnvironmentalResults;
  efficiency: EfficiencyResults;
}

export interface AnalysisResult {
  id: number;
  process: number;
  timestamp: string;
  technical_results: TechnicalResults;
  economic_results: EconomicResults;
  environmental_results: EnvironmentalResults;
  efficiency_results: EfficiencyResults;
}

export interface AnalysisRequest {
  process_type: ProcessType;
  parameters: TechnicalParameters | EconomicParameters | EnvironmentalParameters;
}

export interface AnalysisFilter {
  start_date?: string;
  end_date?: string;
  status?: string;
  type?: string;
}
