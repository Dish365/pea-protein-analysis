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
}

export interface TechnicalResults {
  protein_recovery: ProteinRecovery;
  separation_efficiency: number;
  process_efficiency: number;
  particle_size_distribution: ParticleSizeDistribution;
}

export interface TechnicalAnalysis extends TechnicalParameters {
  results?: TechnicalResults;
} 