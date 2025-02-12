import { ProcessType } from './process';

export interface EmissionFactors {
  electricity: number; // kg CO2e/kWh
  water: number; // kg CO2e/m3
  transport: number; // kg CO2e/km
  waste: number; // kg CO2e/kg
}

export interface EnvironmentalParameters {
  processType: ProcessType;
  productionVolume: number;
  electricityConsumption: number;
  waterConsumption: number;
  naturalGasConsumption: number;
  wasteGeneration: number;
  transportDistance: number;
  packagingMaterial: string;
  recycledContent: number;
}

export interface EnvironmentalAnalysisResult {
  impact_assessment: {
    gwp: number;
    hct: number;
    frs: number;
  };
  consumption_metrics: {
    electricity: number | null;
    cooling: number | null;
    water: number | null;
  };
  allocated_impacts: {
    method: string;
    factors: Record<string, number>;
    results: Record<string, Record<string, number>>;
  };
}

export interface EmissionsBreakdown {
  electricity: number;
  heating: number;
  cooling: number;
  transport: number;
  waste: number;
}

export interface ResourceConsumption {
  water: number;
  electricity: number;
  naturalGas: number;
  compressedAir: number;
  cooling: number | null;
}

export interface EnvironmentalResults {
  carbonFootprint: number;
  waterFootprint: number;
  energyEfficiency: number;
  emissionsBreakdown: EmissionsBreakdown;
  resourceConsumption: ResourceConsumption;
  wasteRecyclingRate: number;
  toxicityScore: number;
  resourceDepletion: number;
  processType: string;
  allocationMethod: string;
  allocationFactors: Record<string, number>;
  allocatedImpacts: Record<string, {
    gwp: number;
    hct: number;
    frs: number;
  }>;
}

export interface EnvironmentalAnalysis {
  parameters: EnvironmentalParameters;
  results?: EnvironmentalResults;
} 