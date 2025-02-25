// Enums
export type ProcessType = 'baseline' | 'rf' | 'ir';

// Component Interfaces
export interface ProteinRecovery {
  /** Recovery rate in percentage */
  recovery_rate: number;
  /** Protein loss in kg */
  protein_loss: number;
  /** Concentration factor */
  concentration_factor: number;
  /** Moisture compensation factor */
  moisture_compensation_factor: number;
  /** Process efficiency in percentage */
  process_efficiency: number;
  /** Yield gap in percentage */
  yield_gap: number;
  /** Improvement potential in percentage */
  improvement_potential: number;
}

export interface ComponentRecoveries {
  /** Protein recovery in percentage */
  protein: number;
  /** Starch recovery in percentage */
  starch: number;
  /** Fiber recovery in percentage */
  fiber: number;
  /** Others recovery in percentage */
  others: number;
}

export interface SeparationMetrics {
  /** Separation factor */
  separation_factor: number;
  /** Protein enrichment factor */
  protein_enrichment: number;
  /** Separation efficiency in percentage */
  separation_efficiency: number;
  /** Component-wise recovery rates */
  component_recoveries: ComponentRecoveries;
  /** Processing moisture content in percentage */
  processing_moisture: number;
  /** Moisture impact factor */
  moisture_impact: number;
  /** Optimal moisture content in percentage */
  optimal_moisture: number;
  /** Moisture impact factor on efficiency */
  moisture_impact_factor: number;
  /** Cumulative efficiency in percentage */
  cumulative_efficiency: number;
  /** Cumulative enrichment factor */
  cumulative_enrichment: number;
  /** Average step efficiency in percentage */
  average_step_efficiency: number;
  /** Purity achievement in percentage */
  purity_achievement: number;
}

export interface ParticleMetrics {
  /** 10th percentile diameter in μm */
  D10: number;
  /** 50th percentile diameter in μm */
  D50: number;
  /** 90th percentile diameter in μm */
  D90: number;
  /** Distribution span */
  span: number;
  /** Mean particle size in μm */
  mean: number;
  /** Standard deviation of particle size */
  std_dev: number;
  /** Coefficient of variation */
  cv: number;
  /** Specific surface area in m²/g */
  specific_surface_area: number;
  /** Total surface area in m² */
  total_surface_area: number;
  /** Mean surface area in m² */
  mean_surface_area: number;
  /** Pre-treatment moisture content in percentage */
  pre_treatment_moisture: number;
  /** Post-treatment moisture content in percentage */
  post_treatment_moisture: number;
  /** Processing moisture content in percentage */
  processing_moisture: number;
  /** Current moisture content in percentage */
  current_moisture: number;
  /** 10th percentile diameter in μm (alternative notation) */
  d10: number;
  /** 50th percentile diameter in μm (alternative notation) */
  d50: number;
  /** 90th percentile diameter in μm (alternative notation) */
  d90: number;
  /** Overall quality score */
  overall: number;
}

export interface ProcessPerformance {
  /** Cumulative efficiency in percentage */
  cumulative_efficiency: number;
  /** Average step efficiency in percentage */
  average_step_efficiency: number;
  /** Purity achievement in percentage */
  purity_achievement: number;
}

// Input Parameter Interfaces
export interface FeedComposition {
  /** Protein content in percentage */
  protein: number;
  /** Starch content in percentage */
  starch: number;
  /** Fiber content in percentage */
  fiber: number;
  /** Others content in percentage */
  others: number;
}

export interface MassFlow {
  /** Input mass in kg */
  input: number;
  /** Output mass in kg */
  output: number;
}

export interface ProcessData {
  /** Feed composition data */
  feed_composition: FeedComposition;
  /** Product composition data */
  product_composition: FeedComposition;
  /** Mass flow data */
  mass_flow: MassFlow;
  /** Processing moisture content in percentage */
  processing_moisture: number;
}

export interface TargetRanges {
  /** Target range for D10 [min, max] in μm */
  D10: [number, number];
  /** Target range for D50 [min, max] in μm */
  D50: [number, number];
  /** Target range for D90 [min, max] in μm */
  D90: [number, number];
  /** Target range for span [min, max] */
  span: [number, number];
}

// Main Input Interfaces
export interface TechnicalParameters {
  // Recovery Input
  /** Input mass in kg */
  input_mass: number;
  /** Output mass in kg */
  output_mass: number;
  /** Initial protein content in percentage */
  initial_protein_content: number;
  /** Output protein content in percentage */
  output_protein_content: number;
  /** Process type (baseline/rf/ir) */
  process_type: ProcessType;
  /** Moisture compensation factor */
  moisture_compensation_factor: number;
  /** Initial moisture content in percentage */
  initial_moisture: number;
  /** Final moisture content in percentage */
  final_moisture: number;

  // Separation Input
  /** Feed composition data */
  feed_composition: FeedComposition;
  /** Product composition data */
  product_composition: FeedComposition;
  /** Mass flow data */
  mass_flow: MassFlow;
  /** Process step data */
  process_data: ProcessData[];
  /** Target protein purity in percentage */
  target_purity: number;

  // Particle Input
  /** Particle sizes [D10, D50, D90] in μm */
  particle_sizes: number[];
  /** Distribution weights for particle sizes */
  weights: number[];
  /** Particle density in g/cm³ */
  density: number;
  /** Target ranges for particle size distribution */
  target_ranges: TargetRanges;
  /** Treatment type (baseline/rf/ir) */
  treatment_type: ProcessType;
}

// Results Interface
export interface TechnicalResults {
  /** Protein recovery metrics */
  recovery_metrics: ProteinRecovery;
  /** Separation efficiency metrics */
  separation_metrics: SeparationMetrics;
  /** Particle size analysis metrics */
  particle_metrics: ParticleMetrics;
  /** Overall process performance metrics */
  process_performance?: ProcessPerformance;
}

// Main Analysis Interface
export interface TechnicalAnalysis {
  /** Technical analysis parameters */
  parameters: TechnicalParameters;
  /** Technical analysis results */
  results?: TechnicalResults;
} 