export interface AnalysisResult {
  id: string;
  status: "pending" | "running" | "completed" | "failed";
  createdAt: string;
  updatedAt: string;
  results?: any; // Specific analysis results structure
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
