import { ProcessType, ProcessTypeValues } from './process';

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
  processType: ProcessTypeValues;
  airFlow: number;
  classifierSpeed: number;
  
  // Mass Balance
  inputMass: number;
  outputMass: number;
  
  // Content Analysis
  initialProteinContent: number;
  finalProteinContent: number;
  initialMoistureContent: number;
  finalMoistureContent: number;
  
  // Particle Size Analysis
  d10ParticleSize: number;
  d50ParticleSize: number;
  d90ParticleSize: number;
}

export interface TechnicalResults {
  proteinRecovery: ProteinRecovery;
  separationEfficiency: number;
  processEfficiency: number;
  particleSizeDistribution: ParticleSizeDistribution;
}

export interface TechnicalAnalysis {
  parameters: TechnicalParameters;
  results?: TechnicalResults;
} 