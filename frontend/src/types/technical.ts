import { ProcessType } from './process';

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

export interface TechnicalParameters {
  processType: ProcessType;
  airFlowRate: number;
  temperature: number;
  pressure: number;
  inputMass: number;
  outputMass: number;
  initialProteinContent: number;
  targetProteinContent: number;
}

export interface TechnicalResults {
  efficiency: number;
  yieldRate: number;
  proteinRecovery: number;
  energyConsumption: number;
  processTime: number;
  qualityScore: number;
}

export interface TechnicalAnalysis {
  parameters: TechnicalParameters;
  results?: TechnicalResults;
} 