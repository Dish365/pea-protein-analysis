export interface EmissionFactors {
  electricity: number; // kg CO2e/kWh
  water: number; // kg CO2e/m3
  transport: number; // kg CO2e/km
  waste: number; // kg CO2e/kg
}

export interface EnvironmentalParameters {
  production_volume: number;
  
  // Resource Consumption
  electricity_consumption: number;
  cooling_consumption: number;
  water_consumption: number;
  transport_consumption: number;
  equipment_mass: number;
  thermal_ratio: number;
  
  // Allocation Configuration
  allocation_method: 'economic' | 'physical' | 'hybrid';
  hybrid_weights: Record<string, number>;
}

export interface ConsumptionMetrics {
  electricity: number | null;
  cooling: number | null;
  water: number | null;
}

export interface ImpactAssessment {
  gwp: number; // Global Warming Potential
  hct: number; // Human Toxicity
  frs: number; // Fossil Resource Scarcity
}

export interface EnvironmentalResults {
  impact_assessment: ImpactAssessment;
  consumption_metrics: ConsumptionMetrics;
  allocated_impacts: {
    method: string;
    factors: Record<string, number>;
    results: Record<string, ImpactAssessment>;
  };
  energy_efficiency: number;
  resource_depletion: number;
  waste_recycling_rate: number;
}

export interface EnvironmentalAnalysis {
  parameters: EnvironmentalParameters;
  results?: EnvironmentalResults;
}

export interface ProcessInputs {
  // RF Pretreatment Parameters
  rf_electricity_kwh: number;
  rf_temperature_outfeed_c: number;
  rf_temperature_electrode_c: number;
  rf_frequency_mhz: number;
  rf_anode_current_a: number;
  rf_grid_current_a: number;
  
  // Process Steps Energy Consumption
  air_classifier_milling_kwh: number;
  air_classification_kwh: number;
  hammer_milling_kwh: number;
  dehulling_kwh: number;
  
  // Water and Moisture Management
  tempering_water_kg: number;
  initial_moisture_content: number;
  final_moisture_content: number;
  target_moisture_content: number;
  
  // Production Parameters
  product_kg: number;
  equipment_kg: number;
  waste_kg: number;
  transport_ton_km: number;
  
  // Process Configuration
  conveyor_speed_m_min: number;
  material_depth_mm: number;
  electrode_gap_mm: number;
  thermal_ratio: number;
}

export interface ProcessContribution {
  value: number;
  unit: string;
  process: string;
}

export interface ImpactContributions {
  gwp: Record<string, ProcessContribution>;
  hct: Record<string, ProcessContribution>;
  frs: Record<string, ProcessContribution>;
  water: Record<string, ProcessContribution>;
}

export interface TotalImpacts {
  gwp: number; // kg CO2 eq
  hct: number; // CTUh
  frs: number; // kg oil eq
  water_consumption: number; // kg
}

export interface ProcessMetadata {
  total_mass: number;
  energy_intensity: number;
  water_intensity: number;
  thermal_ratio: number;
}

export interface RFParameters {
  temperature_outfeed: number;
  temperature_electrode: number;
  energy_consumption: number;
  contribution_percentage: number;
}

export interface ProcessBreakdown {
  air_classifier_milling: number;
  air_classification: number;
  rf_treatment: number;
  tempering: number;
  hammer_milling: number;
  dehulling: number;
}

export interface RFValidationMetric {
  value: number;
  within_range: boolean;
  optimal: number;
  tolerance: string;
}

export interface MoistureValidation {
  initial: number;
  final: number;
  target: number;
  reduction: number;
  within_range: boolean;
  optimal_reduction: number;
  tolerance: string;
}

export interface RFValidation {
  temperature: {
    outfeed: RFValidationMetric;
    electrode: RFValidationMetric;
  };
  moisture: MoistureValidation;
  energy_efficiency: RFValidationMetric;
  process_contribution: number;
}

export interface ImpactResults {
  total_impacts: TotalImpacts;
  process_contributions: ImpactContributions;
  metadata: ProcessMetadata;
  rf_parameters: RFParameters;
  process_breakdown: ProcessBreakdown;
}

export interface AllocationResults {
  allocation_factors: Record<string, number>;
  allocated_impacts: {
    gwp: Record<string, number>;
    hct: Record<string, number>;
    frs: Record<string, number>;
    water_consumption: Record<string, number>;
  };
  method_used: 'economic' | 'physical' | 'hybrid';
}

export interface EnvironmentalAnalysisRequest {
  request: ProcessInputs;
  allocation_method: 'economic' | 'physical' | 'hybrid';
  product_values: Record<string, number>;
  mass_flows: Record<string, number>;
  hybrid_weights: {
    economic: number;
    physical: number;
  };
}

export interface EnvironmentalAnalysisResponse {
  status: string;
  impact_results: ImpactResults;
  allocation_results: AllocationResults;
  suggested_allocation_method: 'economic' | 'physical' | 'hybrid';
  rf_validation: RFValidation;
} 