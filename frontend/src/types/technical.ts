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
  // Process Parameters
  process_type: ProcessTypeValues;
  air_flow: number;
  classifier_speed: number;
  
  // Mass Balance
  input_mass: number;
  output_mass: number;
  
  // Content Analysis
  initial_protein_content: number;
  final_protein_content: number;
  initial_moisture_content: number;
  final_moisture_content: number;
  
  // Particle Size Analysis
  d10_particle_size: number;
  d50_particle_size: number;
  d90_particle_size: number;

  // Process-specific parameters (optional based on process type)
  electricity_consumption?: number;
  cooling_consumption?: number;
  water_consumption?: number;
  transport_consumption?: number;
  equipment_mass?: number;
  thermal_ratio?: number;
}

export interface TechnicalResults {
  protein_recovery: ProteinRecovery;
  separation_efficiency: number;
  process_efficiency: number;
  particle_size_distribution: ParticleSizeDistribution;
}

export interface TechnicalAnalysis {
  parameters: TechnicalParameters;
  results?: TechnicalResults;
} 