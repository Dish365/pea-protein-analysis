import { TechnicalParameters } from './technical';
import { z } from "zod";

export enum ProcessStatus {
  PENDING = 'pending',
  PROCESSING = 'processing',
  COMPLETED = 'completed',
  FAILED = 'failed'
}

// Process type definitions
export const ProcessTypeEnum = {
  BASELINE: 'baseline',
  RF: 'rf',
  IR: 'ir'
} as const;

export type ProcessType = typeof ProcessTypeEnum[keyof typeof ProcessTypeEnum];

export type ProcessTypeValues = 'baseline' | 'rf' | 'ir';

export interface Equipment {
  name: string;
  cost: number;
  efficiency: number;
  maintenance_cost: number;
  energy_consumption: number;
  processing_capacity: number;
}

export interface Utility {
  name: string;
  consumption: number;
  unit_price: number;
  unit: string;
}

export interface RawMaterial {
  name: string;
  quantity: number;
  unit_price: number;
  unit: string;
}

export interface LaborConfig {
  hourly_wage: number;
  hours_per_week: number;
  weeks_per_year: number;
  num_workers: number;
}

export interface IndirectFactor {
  name: string;
  cost: number;
  percentage: number;
}

export interface ResourceConfiguration {
  equipment: Equipment[];
  utilities: Utility[];
  raw_materials: RawMaterial[];
  labor_config: LaborConfig;
  indirect_factors: IndirectFactor[];
}

export interface AllocationConfiguration {
  allocation_method: 'economic' | 'physical' | 'hybrid';
  hybrid_weights: Record<string, number>;
}

export interface RiskConfiguration {
  sensitivity_range: number;
  steps: number;
}

export interface ProcessAnalysis {
  id: string;
  process_type: ProcessType;
  timestamp: string;
  status: ProcessStatus;
  progress: number;
  
  // Technical Analysis Inputs
  air_flow: number;
  classifier_speed: number;
  input_mass: number;
  output_mass: number;
  initial_protein_content: number;
  final_protein_content: number;
  initial_moisture_content: number;
  final_moisture_content: number;
  d10_particle_size: number;
  d50_particle_size: number;
  d90_particle_size: number;
  
  // Economic Analysis Inputs
  equipment: Equipment[];
  equipment_cost: number;
  maintenance_cost: number;
  installation_factor: number;
  indirect_costs_factor: number;
  maintenance_factor: number;
  indirect_factors: IndirectFactor[];
  raw_material_cost: number;
  utility_cost: number;
  labor_cost: number;
  utilities: Utility[];
  raw_materials: RawMaterial[];
  labor_config: LaborConfig;
  project_duration: number;
  discount_rate: number;
  production_volume: number;
  revenue_per_year: number;
  cash_flows: number[];
  
  // Risk Analysis
  sensitivity_range: number;
  steps: number;
  
  // Environmental Analysis Inputs
  electricity_consumption: number;
  cooling_consumption: number;
  water_consumption: number;
  transport_consumption: number;
  equipment_mass: number;
  thermal_ratio: number;
  energy_consumption: Record<string, number>;
  production_data: Record<string, any>;
  product_values: Record<string, any>;
  
  // Allocation Configuration
  allocation_method: 'economic' | 'physical' | 'hybrid';
  hybrid_weights: Record<string, number>;
  
  // Results
  technical_results?: Record<string, any>;
  economic_results?: Record<string, any>;
  environmental_results?: Record<string, any>;
  efficiency_results?: Record<string, any>;
}

// Base schemas for validation
export const technicalSchema = z.object({
  process_type: z.nativeEnum(ProcessTypeEnum),
  air_flow: z.number().min(0).max(1000)
    .describe("The volumetric flow rate of air through the system"),
  classifier_speed: z.number().min(0)
    .describe("The rotational speed of the classifier wheel"),
  input_mass: z.number().min(0).max(10000)
    .describe("Total mass of feed material entering the process"),
  output_mass: z.number().min(0).max(10000)
    .describe("Total mass of product material after processing"),
  initial_protein_content: z.number().min(0).max(100)
    .describe("Protein content in the feed material"),
  final_protein_content: z.number().min(0).max(100)
    .describe("Protein content in the product material"),
  initial_moisture_content: z.number().min(0).max(100)
    .describe("Moisture content in the feed material"),
  final_moisture_content: z.number().min(0).max(100)
    .describe("Moisture content in the product material"),
  d10_particle_size: z.number().min(0)
    .describe("Particle size at which 10% of the sample is comprised of smaller particles"),
  d50_particle_size: z.number().min(0)
    .describe("Median particle size (50% of particles are smaller)"),
  d90_particle_size: z.number().min(0)
    .describe("Particle size at which 90% of the sample is comprised of smaller particles"),
  electricity_consumption: z.number().min(0).optional(),
  cooling_consumption: z.number().min(0).optional(),
  water_consumption: z.number().min(0).optional()
}).refine(
  (data) => data.output_mass <= data.input_mass,
  {
    message: "Output mass cannot exceed input mass",
    path: ["output_mass"]
  }
).refine(
  (data) => data.final_moisture_content <= data.initial_moisture_content,
  {
    message: "Final moisture content cannot be higher than initial moisture content",
    path: ["final_moisture_content"]
  }
).refine(
  (data) => data.d50_particle_size >= data.d10_particle_size,
  {
    message: "D50 must be greater than or equal to D10",
    path: ["d50_particle_size"]
  }
).refine(
  (data) => data.d90_particle_size >= data.d50_particle_size,
  {
    message: "D90 must be greater than or equal to D50",
    path: ["d90_particle_size"]
  }
).refine(
  (data) => {
    if (data.process_type === ProcessTypeEnum.RF) {
      return data.electricity_consumption !== undefined && data.electricity_consumption > 0;
    }
    if (data.process_type === ProcessTypeEnum.IR) {
      return data.cooling_consumption !== undefined && data.cooling_consumption > 0;
    }
    return true;
  },
  {
    message: "Process type specific requirements not met",
    path: ["process_type"]
  }
);

export const economicSchema = z.object({
  production_volume: z.number().min(0),
  operating_hours: z.number().min(0).max(8760),
  equipment_cost: z.number().min(0),
  utility_cost: z.number().min(0),
  raw_material_cost: z.number().min(0),
  labor_cost: z.number().min(0),
  maintenance_factor: z.number().min(0).max(1),
  indirect_costs_factor: z.number().min(0).max(1),
  installation_factor: z.number().min(0).max(1),
  project_duration: z.number().min(1).max(50),
  discount_rate: z.number().min(0).max(1),
  revenue_per_year: z.number().min(0)
});

export const environmentalSchema = z.object({
  electricity_consumption: z.number().min(0),
  cooling_consumption: z.number().min(0),
  water_consumption: z.number().min(0),
  transport_consumption: z.number().min(0),
  equipment_mass: z.number().min(0),
  thermal_ratio: z.number().min(0).max(1),
  allocation_method: z.enum(['economic', 'physical', 'hybrid'] as const),
  hybrid_weights: z.record(z.string(), z.number().min(0).max(1)).optional()
});

// Combined schema for the entire process
export const processSchema = z.object({
  technical: technicalSchema,
  economic: economicSchema,
  environmental: environmentalSchema
});

// Utility type for required fields based on process type
export const getRequiredFields = (processType: 'baseline' | 'rf' | 'ir') => {
  const baseFields = [
    'process_type', 'air_flow', 'classifier_speed', 'input_mass', 'output_mass',
    'initial_protein_content', 'final_protein_content', 'initial_moisture_content',
    'final_moisture_content', 'd10_particle_size', 'd50_particle_size', 'd90_particle_size'
  ];

  if (processType === 'rf') {
    return [...baseFields, 'electricity_consumption', 'water_consumption'];
  }
  if (processType === 'ir') {
    return [...baseFields, 'cooling_consumption', 'water_consumption'];
  }
  return baseFields;
};

// Types
export type ProcessTypeValue = z.infer<typeof technicalSchema>['process_type'];
export type TechnicalData = z.infer<typeof technicalSchema>;
export type EconomicData = z.infer<typeof economicSchema>;
export type EnvironmentalData = z.infer<typeof environmentalSchema>;
export type ProcessData = z.infer<typeof processSchema>;

// Validation helper
export const validateProcessData = (data: ProcessData): string[] => {
  const errors: string[] = [];
  
  // Validate technical data
  const technicalResult = technicalSchema.safeParse(data.technical);
  if (!technicalResult.success) {
    errors.push(...technicalResult.error.errors.map(e => `Technical: ${e.message}`));
  }

  // Validate economic data
  const economicResult = economicSchema.safeParse(data.economic);
  if (!economicResult.success) {
    errors.push(...economicResult.error.errors.map(e => `Economic: ${e.message}`));
  }

  // Validate environmental data
  const environmentalResult = environmentalSchema.safeParse(data.environmental);
  if (!environmentalResult.success) {
    errors.push(...environmentalResult.error.errors.map(e => `Environmental: ${e.message}`));
  }

  return errors;
};

