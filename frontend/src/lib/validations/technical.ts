import * as z from "zod";

export const technicalValidationSchema = z.object({
  // Recovery Input
  input_mass: z.number().gt(0).describe("Input mass in kg"),
  output_mass: z.number().gt(0).describe("Output mass in kg"),
  initial_protein_content: z.number().gt(0).max(100).describe("Initial protein content in %"),
  output_protein_content: z.number().gt(0).max(100).describe("Output protein content in %"),
  process_type: z.enum(['baseline', 'rf', 'ir']).describe("Process type (baseline/rf/ir)"),
  moisture_compensation_factor: z.number().min(0).max(0.2).default(0.05).describe("Moisture compensation factor"),
  initial_moisture: z.number().min(0).max(100).default(13.6).describe("Initial moisture content percentage"),
  final_moisture: z.number().min(0).max(100).default(10.2).describe("Final moisture content percentage"),

  // Separation Input
  feed_composition: z.object({
    protein: z.number().min(0).max(100),
    starch: z.number().min(0).max(100),
    fiber: z.number().min(0).max(100),
    others: z.number().min(0).max(100),
  }).refine(data => {
    const sum = Object.values(data).reduce((a, b) => a + b, 0);
    return Math.abs(sum - 100) <= 0.1;
  }, { message: "Composition percentages must sum to 100%" }),

  product_composition: z.object({
    protein: z.number().min(0).max(100),
    starch: z.number().min(0).max(100),
    fiber: z.number().min(0).max(100),
    others: z.number().min(0).max(100),
  }).refine(data => {
    const sum = Object.values(data).reduce((a, b) => a + b, 0);
    return Math.abs(sum - 100) <= 0.1;
  }, { message: "Composition percentages must sum to 100%" }),

  mass_flow: z.object({
    input: z.number().gt(0),
    output: z.number().gt(0),
  }).refine(data => data.output <= data.input, {
    message: "Output mass cannot be greater than input mass"
  }),

  process_data: z.array(z.object({
    feed_composition: z.object({
      protein: z.number().min(0).max(100),
      starch: z.number().min(0).max(100),
      fiber: z.number().min(0).max(100),
      others: z.number().min(0).max(100),
    }).refine(data => {
      const sum = Object.values(data).reduce((a, b) => a + b, 0);
      return Math.abs(sum - 100) <= 0.1;
    }, { message: "Process data feed composition percentages must sum to 100%" }),
    product_composition: z.object({
      protein: z.number().min(0).max(100),
      starch: z.number().min(0).max(100),
      fiber: z.number().min(0).max(100),
      others: z.number().min(0).max(100),
    }).refine(data => {
      const sum = Object.values(data).reduce((a, b) => a + b, 0);
      return Math.abs(sum - 100) <= 0.1;
    }, { message: "Process data product composition percentages must sum to 100%" }),
    mass_flow: z.object({
      input: z.number().gt(0),
      output: z.number().gt(0),
    }).refine(data => data.output <= data.input, {
      message: "Process data output mass cannot be greater than input mass"
    }),
    processing_moisture: z.number().min(0).max(100),
  })),
  target_purity: z.number().min(0).max(100),

  // Particle Input
  particle_sizes: z.array(z.number().gt(0).max(10000))
    .length(3)
    .describe("Particle sizes in μm (D10, D50, D90)"),
  weights: z.array(z.number().min(0).max(1))
    .length(3)
    .refine(data => Math.abs(data.reduce((a, b) => a + b, 0) - 1.0) <= 0.001, {
      message: "Weights must sum to 1"
    }),
  density: z.number().gt(0).lt(10).describe("Particle density in g/cm³"),
  target_ranges: z.object({
    D10: z.tuple([z.number().min(0).max(10000), z.number().min(0).max(10000)]),
    D50: z.tuple([z.number().min(0).max(10000), z.number().min(0).max(10000)]),
    D90: z.tuple([z.number().min(0).max(10000), z.number().min(0).max(10000)]),
    span: z.tuple([z.number().min(0), z.number().min(0)]),
  }).refine(data => {
    return Object.entries(data).every(([_, [min, max]]) => min < max);
  }, { message: "Min value must be less than max value for all ranges" }),
  treatment_type: z.enum(['baseline', 'rf', 'ir']),
}); 