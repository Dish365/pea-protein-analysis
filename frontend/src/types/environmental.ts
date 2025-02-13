import { ProcessType, ProcessTypeValues } from './process';

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