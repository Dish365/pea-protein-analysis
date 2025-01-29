export interface EmissionFactors {
  electricity: number; // kg CO2e/kWh
  water: number; // kg CO2e/m3
  transport: number; // kg CO2e/km
  waste: number; // kg CO2e/kg
}

export interface EnvironmentalParameters {
  // Energy Consumption
  electricity_consumption: number;
  thermal_energy: number;
  cooling_consumption: number;
  
  // Water Usage
  water_consumption: number;
  wastewater_generation: number;
  
  // Waste Management
  solid_waste: number;
  recyclable_waste: number;
  
  // Transportation
  transport_distance: number;
  transport_load: number;
  equipment_mass: number;
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