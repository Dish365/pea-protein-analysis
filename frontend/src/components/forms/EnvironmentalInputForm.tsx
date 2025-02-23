import React from 'react';
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import * as z from "zod";
import { Form } from "@/components/ui/form";
import { Button } from "@/components/ui/button";
import { Alert } from "@/components/ui/alert";
import { FormSection } from "./shared/FormSection";
import { FormNumberInput } from "./shared/FormNumberInput";
import { FormSelect } from "./shared/FormSelect";
import { 
  EnvironmentalAnalysisRequest,
  ProcessInputs,
} from '../../types/environmental';

const defaultProcessInputs: ProcessInputs = {
  // RF Pretreatment Parameters
  rf_electricity_kwh: 150.0,
  rf_temperature_outfeed_c: 84.4,
  rf_temperature_electrode_c: 100.1,
  rf_frequency_mhz: 27.12,
  rf_anode_current_a: 1.79,
  rf_grid_current_a: 0.56,
  
  // Process Steps Energy Consumption
  air_classifier_milling_kwh: 250.0,
  air_classification_kwh: 250.0,
  hammer_milling_kwh: 150.0,
  dehulling_kwh: 150.0,
  
  // Water and Moisture Management
  tempering_water_kg: 800.0,
  initial_moisture_content: 0.136,
  final_moisture_content: 0.102,
  target_moisture_content: 0.125,
  
  // Production Parameters
  product_kg: 1500.0,
  equipment_kg: 8500.0,
  waste_kg: 450.0,
  transport_ton_km: 1200.0,
  
  // Process Configuration
  conveyor_speed_m_min: 0.17,
  material_depth_mm: 30.0,
  electrode_gap_mm: 86.9,
  thermal_ratio: 0.65,
};

const defaultAllocationValues = {
  product_values: {
    protein_concentrate: 6.50,
    starch: 2.30,
    fiber: 1.80,
  },
  mass_flows: {
    protein_concentrate: 219.0,
    starch: 600.0,
    fiber: 181.0,
  },
  hybrid_weights: {
    economic: 0.6,
    physical: 0.4,
  },
};

const allocationMethodOptions = [
  { value: 'economic', label: 'Economic' },
  { value: 'physical', label: 'Physical' },
  { value: 'hybrid', label: 'Hybrid' },
];

// Form validation schema
const formSchema = z.object({
  // RF Pretreatment Parameters
  rf_electricity_kwh: z.number().min(0),
  rf_temperature_outfeed_c: z.number().min(80).max(90),
  rf_temperature_electrode_c: z.number().min(95).max(105),
  rf_frequency_mhz: z.number().min(0),
  rf_anode_current_a: z.number().min(0),
  rf_grid_current_a: z.number().min(0),
  
  // Process Steps Energy
  air_classifier_milling_kwh: z.number().min(0),
  air_classification_kwh: z.number().min(0),
  hammer_milling_kwh: z.number().min(0),
  dehulling_kwh: z.number().min(0),
  
  // Water and Moisture
  tempering_water_kg: z.number().min(0),
  initial_moisture_content: z.number().min(0).max(1),
  final_moisture_content: z.number().min(0).max(1),
  target_moisture_content: z.number().min(0).max(1),
  
  // Production Parameters
  product_kg: z.number().min(0),
  equipment_kg: z.number().min(0),
  waste_kg: z.number().min(0),
  transport_ton_km: z.number().min(0),
  
  // Process Configuration
  conveyor_speed_m_min: z.number().min(0),
  material_depth_mm: z.number().min(0),
  electrode_gap_mm: z.number().min(0),
  thermal_ratio: z.number().min(0).max(1),
  
  // Allocation
  allocation_method: z.enum(['economic', 'physical', 'hybrid']),
  product_values: z.record(z.number().min(0)),
  mass_flows: z.record(z.number().min(0)),
  hybrid_weights: z.object({
    economic: z.number().min(0).max(1),
    physical: z.number().min(0).max(1),
  }),
});

interface EnvironmentalInputFormProps {
  onSubmit: (data: EnvironmentalAnalysisRequest) => void;
  isLoading?: boolean;
}

export function EnvironmentalInputForm({
  onSubmit,
  isLoading = false,
}: EnvironmentalInputFormProps) {
  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      ...defaultProcessInputs,
      allocation_method: 'economic',
      product_values: defaultAllocationValues.product_values,
      mass_flows: defaultAllocationValues.mass_flows,
      hybrid_weights: defaultAllocationValues.hybrid_weights,
    },
  });

  const handleSubmit = (values: z.infer<typeof formSchema>) => {
    const requestData: EnvironmentalAnalysisRequest = {
      request: {
        ...values,
        rf_electricity_kwh: values.rf_electricity_kwh,
        rf_temperature_outfeed_c: values.rf_temperature_outfeed_c,
        rf_temperature_electrode_c: values.rf_temperature_electrode_c,
        // ... other process inputs
      },
      allocation_method: values.allocation_method,
      product_values: values.product_values,
      mass_flows: values.mass_flows,
      hybrid_weights: values.hybrid_weights,
    };
    
    onSubmit(requestData);
  };

  const allocationMethod = form.watch('allocation_method');

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(handleSubmit)} className="space-y-8">
        <FormSection 
          title="RF Pretreatment Parameters"
          tooltip="Radio Frequency treatment parameters for pea protein processing"
        >
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            <FormNumberInput
              name="rf_electricity_kwh"
              label="RF Electricity"
              unit="kWh"
              tooltip="Radio frequency unit power consumption"
              required
            />
            <FormNumberInput
              name="rf_temperature_outfeed_c"
              label="Outfeed Temperature"
              unit="°C"
              tooltip="Temperature at outfeed (optimal: 80-90°C)"
              min={80}
              max={90}
              required
            />
            <FormNumberInput
              name="rf_temperature_electrode_c"
              label="Electrode Temperature"
              unit="°C"
              tooltip="Electrode temperature (optimal: 95-105°C)"
              min={95}
              max={105}
              required
            />
            <FormNumberInput
              name="rf_frequency_mhz"
              label="RF Frequency"
              unit="MHz"
              tooltip="Operating frequency of RF unit"
              required
            />
            <FormNumberInput
              name="rf_anode_current_a"
              label="Anode Current"
              unit="A"
              tooltip="Anode current measurement"
              required
            />
            <FormNumberInput
              name="rf_grid_current_a"
              label="Grid Current"
              unit="A"
              tooltip="Grid current measurement"
              required
            />
          </div>
        </FormSection>

        <FormSection 
          title="Process Steps Energy Consumption"
          tooltip="Energy consumption for each processing step"
        >
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            <FormNumberInput
              name="air_classifier_milling_kwh"
              label="Air Classifier Milling"
              unit="kWh"
              tooltip="Energy consumption for air classifier milling"
              required
            />
            <FormNumberInput
              name="air_classification_kwh"
              label="Air Classification"
              unit="kWh"
              tooltip="Energy consumption for air classification"
              required
            />
            <FormNumberInput
              name="hammer_milling_kwh"
              label="Hammer Milling"
              unit="kWh"
              tooltip="Energy consumption for hammer milling"
              required
            />
            <FormNumberInput
              name="dehulling_kwh"
              label="Dehulling"
              unit="kWh"
              tooltip="Energy consumption for dehulling"
              required
            />
          </div>
        </FormSection>

        <FormSection 
          title="Water and Moisture Management"
          tooltip="Water usage and moisture content parameters"
        >
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            <FormNumberInput
              name="tempering_water_kg"
              label="Tempering Water"
              unit="kg"
              tooltip="Water used in tempering process"
              required
            />
            <FormNumberInput
              name="initial_moisture_content"
              label="Initial Moisture"
              tooltip="Initial moisture content (0-1)"
              step={0.001}
              min={0}
              max={1}
              required
            />
            <FormNumberInput
              name="final_moisture_content"
              label="Final Moisture"
              tooltip="Final moisture content (0-1)"
              step={0.001}
              min={0}
              max={1}
              required
            />
            <FormNumberInput
              name="target_moisture_content"
              label="Target Moisture"
              tooltip="Target moisture content (0-1)"
              step={0.001}
              min={0}
              max={1}
              required
            />
          </div>
        </FormSection>

        <FormSection 
          title="Allocation Configuration"
          tooltip="Configure how environmental impacts are allocated between products"
        >
          <div className="space-y-6">
            <FormSelect
              name="allocation_method"
              label="Allocation Method"
              options={allocationMethodOptions}
              tooltip="Method used to allocate environmental impacts"
              required
            />

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {Object.keys(defaultAllocationValues.product_values).map((key) => (
                <FormNumberInput
                  key={key}
                  name={`product_values.${key}`}
                  label={`${key.replace('_', ' ').toUpperCase()} Value`}
                  tooltip={`Economic value for ${key}`}
                  required
                />
              ))}
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {Object.keys(defaultAllocationValues.mass_flows).map((key) => (
                <FormNumberInput
                  key={key}
                  name={`mass_flows.${key}`}
                  label={`${key.replace('_', ' ').toUpperCase()} Mass Flow`}
                  unit="kg"
                  tooltip={`Mass flow for ${key}`}
                  required
                />
              ))}
            </div>

            {allocationMethod === 'hybrid' && (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <FormNumberInput
                  name="hybrid_weights.economic"
                  label="Economic Weight"
                  tooltip="Weight for economic allocation (0-1)"
                  step={0.1}
                  min={0}
                  max={1}
                  required
                />
                <FormNumberInput
                  name="hybrid_weights.physical"
                  label="Physical Weight"
                  tooltip="Weight for physical allocation (0-1)"
                  step={0.1}
                  min={0}
                  max={1}
                  required
                />
              </div>
            )}
          </div>
        </FormSection>

        <div className="flex justify-end">
          <Button 
            type="submit" 
            disabled={isLoading}
            className="w-full md:w-auto"
          >
            {isLoading ? 'Processing...' : 'Analyze Environmental Impact'}
          </Button>
        </div>

        {Object.keys(form.formState.errors).length > 0 && (
          <Alert variant="destructive">
            Please correct the errors before submitting.
          </Alert>
        )}
      </form>
    </Form>
  );
}

export default EnvironmentalInputForm;
