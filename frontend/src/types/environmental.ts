export interface EmissionFactors {
  electricity: number; // kg CO2e/kWh
  water: number; // kg CO2e/m3
  transport: number; // kg CO2e/km
  waste: number; // kg CO2e/kg
}

export interface EnvironmentalAnalysisResult {
  emissions: {
    electricity: number;
    water: number;
    transport: number;
    waste: number;
    total: number;
  };
  resources: {
    energyConsumption: number; // kWh
    waterConsumption: number; // m3
    materialEfficiency: number; // %
    wasteGeneration: number; // kg
  };
  impacts: {
    carbonFootprint: number; // kg CO2e
    waterFootprint: number; // m3
    energyIntensity: number; // kWh/kg product
    wasteIntensity: number; // kg waste/kg product
  };
  metrics: {
    sustainabilityScore: number; // 0-100
    circularityIndex: number; // 0-1
    resourceEfficiency: number; // %
  };
} 