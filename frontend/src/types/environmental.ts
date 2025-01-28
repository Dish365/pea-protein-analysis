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
  emissions: {
    electricity: number;
    water: number;
    transport: number;
    waste: number;
    total: number;
  };
  resources: {
    energy_consumption: number;
    water_consumption: number;
    material_efficiency: number;
    waste_generation: number;
  };
  impacts: {
    carbon_footprint: number;
    water_footprint: number;
    energy_intensity: number;
    waste_intensity: number;
  };
  metrics: {
    sustainabilityScore: number; // 0-100
    circularityIndex: number; // 0-1
    resourceEfficiency: number; // %
  };
} 