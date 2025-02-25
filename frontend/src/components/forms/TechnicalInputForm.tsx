"use client";

import React, { useEffect } from "react";
import { useForm, FormProvider } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import * as z from "zod";
import { Button } from "@/components/ui/button";
import { TechnicalParameters } from "@/types/technical";
import { FormSection } from "./shared/FormSection";
import { FormNumberInput } from "./shared/FormNumberInput";
import { FormSelect } from "./shared/FormSelect";
import { TooltipProvider } from "@/components/ui/tooltip";
import { Progress } from "@/components/ui/progress";
import { Card } from "@/components/ui/card";
import { technicalValidationSchema } from "@/lib/validations/technical";

const processTypeOptions = [
  { value: 'baseline', label: 'Baseline' },
  { value: 'rf', label: 'RF' },
  { value: 'ir', label: 'IR' }
];

// Default values matching the Python backend exactly
const DEFAULT_TECHNICAL_VALUES: TechnicalParameters = {
  // Recovery Input
  input_mass: 1000.0,
  output_mass: 219.0,
  initial_protein_content: 45.0,
  output_protein_content: 63.1,
  process_type: 'rf',
  moisture_compensation_factor: 0.05,
  initial_moisture: 13.6,
  final_moisture: 10.2,

  // Separation Input
  feed_composition: {
    protein: 45.0,
    starch: 35.0,
    fiber: 15.0,
    others: 5.0
  },
  product_composition: {
    protein: 63.1,
    starch: 22.9,
    fiber: 10.0,
    others: 4.0
  },
  mass_flow: {
    input: 1000.0,
    output: 219.0
  },
  process_data: [{
    feed_composition: {
      protein: 45.0,
      starch: 35.0,
      fiber: 15.0,
      others: 5.0
    },
    product_composition: {
      protein: 63.1,
      starch: 22.9,
      fiber: 10.0,
      others: 4.0
    },
    mass_flow: {
      input: 1000.0,
      output: 219.0
    },
    processing_moisture: 10.2
  }],
  target_purity: 63.1,

  // Particle Input
  particle_sizes: [2.42, 7.14, 17.85],  // D0.1, D0.5, D0.9 for fine fraction
  weights: [0.1, 0.5, 0.4],            // Distribution weights
  density: 1.35,                       // Typical pea protein density g/cm³
  target_ranges: {
    D10: [2.0, 3.0],                // Around measured D0.1 of 2.42
    D50: [7.0, 7.5],                // Around measured D0.5 of 7.14
    D90: [17.0, 18.0],              // Around measured D0.9 of 17.85
    span: [1.5, 2.5]                // Typical range for protein concentrate
  },
  treatment_type: 'rf'
};

interface TechnicalInputFormProps {
  onSubmit: (values: TechnicalParameters) => void;
  isSubmitting?: boolean;
  initialData?: TechnicalParameters;
}

export default function TechnicalInputForm({
  onSubmit,
  isSubmitting = false,
  initialData
}: TechnicalInputFormProps) {
  const form = useForm<TechnicalParameters>({
    resolver: zodResolver(technicalValidationSchema),
    defaultValues: initialData || DEFAULT_TECHNICAL_VALUES,
    mode: "onChange"
  });

  const processType = form.watch('process_type');

  const handleSubmit = async (values: TechnicalParameters) => {
    console.log('Form submitted with values:', values);
    try {
      await onSubmit(values);
    } catch (error) {
      console.error('Form submission error:', error);
    }
  };

  const calculateProgress = () => {
    const fields = Object.keys(form.getValues());
    const values = form.getValues();
    const filledFields = fields.filter(field => {
      const value = values[field as keyof TechnicalParameters];
      return value !== undefined && value !== null && !form.formState.errors[field as keyof TechnicalParameters];
    });
    return (filledFields.length / fields.length) * 100;
  };

  // Log form errors when they change
  useEffect(() => {
    if (Object.keys(form.formState.errors).length > 0) {
      console.log('Form validation errors:', form.formState.errors);
    }
  }, [form.formState.errors]);

  const progress = calculateProgress();

  return (
    <TooltipProvider>
      <FormProvider {...form}>
        <div className="space-y-6 max-w-4xl mx-auto">
          <div className="space-y-2 mb-8">
            <div className="flex justify-between items-center">
              <h2 className="text-lg font-semibold">Technical Analysis Parameters</h2>
              <span className="text-sm text-muted-foreground">
                {Math.round(progress)}% Complete
              </span>
            </div>
            <Progress value={progress} className="h-2" />
          </div>

          <form onSubmit={form.handleSubmit(handleSubmit)} className="space-y-8">
            <div className="grid gap-6">
              {/* Recovery Input Section */}
              <Card className="p-6">
                <FormSection 
                  title="Recovery Parameters" 
                  tooltip="Configure the protein recovery parameters"
                >
                  <div className="grid gap-4 sm:grid-cols-2">
                    <FormSelect
                      name="process_type"
                      label="Process Type"
                      options={processTypeOptions}
                      required
                      tooltip="Select the type of separation process"
                    />
                    <FormNumberInput
                      name="input_mass"
                      label="Input Mass"
                      unit="kg"
                      required
                      tooltip="Total input mass"
                    />
                    <FormNumberInput
                      name="output_mass"
                      label="Output Mass"
                      unit="kg"
                      required
                      tooltip="Output mass of protein concentrate"
                    />
                    <FormNumberInput
                      name="initial_protein_content"
                      label="Initial Protein Content"
                      unit="%"
                      required
                      tooltip="Initial protein content"
                    />
                    <FormNumberInput
                      name="output_protein_content"
                      label="Output Protein Content"
                      unit="%"
                      required
                      tooltip="RF treatment protein purity"
                    />
                    <FormNumberInput
                      name="moisture_compensation_factor"
                      label="Moisture Compensation Factor"
                      step={0.01}
                      required
                      tooltip="Moisture compensation factor"
                    />
                    <FormNumberInput
                      name="initial_moisture"
                      label="Initial Moisture"
                      unit="%"
                      required
                      tooltip="Initial moisture content"
                    />
                    <FormNumberInput
                      name="final_moisture"
                      label="Final Moisture"
                      unit="%"
                      required
                      tooltip="Final moisture content"
                    />
                  </div>
                </FormSection>
              </Card>

              {/* Separation Input Section */}
              <Card className="p-6">
                <FormSection 
                  title="Feed Composition" 
                  tooltip="Input the feed composition parameters"
                >
                  <div className="grid gap-4 sm:grid-cols-2">
                    <FormNumberInput
                      name="feed_composition.protein"
                      label="Protein Content"
                      unit="%"
                      required
                      tooltip="Protein content in feed"
                    />
                    <FormNumberInput
                      name="feed_composition.starch"
                      label="Starch Content"
                      unit="%"
                      required
                      tooltip="Starch content in feed"
                    />
                    <FormNumberInput
                      name="feed_composition.fiber"
                      label="Fiber Content"
                      unit="%"
                      required
                      tooltip="Fiber content in feed"
                    />
                    <FormNumberInput
                      name="feed_composition.others"
                      label="Others Content"
                      unit="%"
                      required
                      tooltip="Other components content in feed"
                    />
                  </div>
                </FormSection>
              </Card>

              <Card className="p-6">
                <FormSection 
                  title="Product Composition" 
                  tooltip="Input the product composition parameters"
                >
                  <div className="grid gap-4 sm:grid-cols-2">
                    <FormNumberInput
                      name="product_composition.protein"
                      label="Protein Content"
                      unit="%"
                      required
                      tooltip="Protein content in product"
                    />
                    <FormNumberInput
                      name="product_composition.starch"
                      label="Starch Content"
                      unit="%"
                      required
                      tooltip="Starch content in product"
                    />
                    <FormNumberInput
                      name="product_composition.fiber"
                      label="Fiber Content"
                      unit="%"
                      required
                      tooltip="Fiber content in product"
                    />
                    <FormNumberInput
                      name="product_composition.others"
                      label="Others Content"
                      unit="%"
                      required
                      tooltip="Other components content in product"
                    />
                  </div>
                </FormSection>
              </Card>

              {/* Particle Analysis Section */}
              <Card className="p-6">
                <FormSection 
                  title="Particle Size Analysis" 
                  tooltip="Configure particle size distribution parameters"
                >
                  <div className="grid gap-4 sm:grid-cols-2">
                    <FormNumberInput
                      name="density"
                      label="Density"
                      unit="g/cm³"
                      required
                      tooltip="Typical pea protein density"
                    />
                    <FormSelect
                      name="treatment_type"
                      label="Treatment Type"
                      options={processTypeOptions}
                      required
                      tooltip="Select the treatment type"
                    />
                    {/* Particle sizes array inputs */}
                    <FormNumberInput
                      name="particle_sizes.0"
                      label="D10 Particle Size"
                      unit="μm"
                      required
                      tooltip="D0.1 for fine fraction"
                    />
                    <FormNumberInput
                      name="particle_sizes.1"
                      label="D50 Particle Size"
                      unit="μm"
                      required
                      tooltip="D0.5 for fine fraction"
                    />
                    <FormNumberInput
                      name="particle_sizes.2"
                      label="D90 Particle Size"
                      unit="μm"
                      required
                      tooltip="D0.9 for fine fraction"
                    />
                    <FormNumberInput
                      name="weights.0"
                      label="D10 Weight"
                      step={0.1}
                      required
                      tooltip="Weight for D10 particle size"
                    />
                    <FormNumberInput
                      name="weights.1"
                      label="D50 Weight"
                      step={0.1}
                      required
                      tooltip="Weight for D50 particle size"
                    />
                    <FormNumberInput
                      name="weights.2"
                      label="D90 Weight"
                      step={0.1}
                      required
                      tooltip="Weight for D90 particle size"
                    />
                  </div>
                </FormSection>
              </Card>

              <Card className="p-6">
                <FormSection title="Target Ranges">
                  <FormNumberInput name="target_ranges.D10.0" label="D10 Min" />
                  <FormNumberInput name="target_ranges.D10.1" label="D10 Max" />
                  <FormNumberInput name="target_ranges.D50.0" label="D50 Min" />
                  <FormNumberInput name="target_ranges.D50.1" label="D50 Max" />
                  <FormNumberInput name="target_ranges.D90.0" label="D90 Min" />
                  <FormNumberInput name="target_ranges.D90.1" label="D90 Max" />
                  <FormNumberInput name="target_ranges.span.0" label="Span Min" />
                  <FormNumberInput name="target_ranges.span.1" label="Span Max" />
                </FormSection>
              </Card>

              <Card className="p-6">
                <FormSection 
                  title="Target Purity"
                >
                  <FormNumberInput 
                    name="target_purity"
                    label="Target Purity"
                    unit="%"
                    required
                  />
                </FormSection>
              </Card>
            </div>

            <div className="flex justify-end">
              <Button 
                type="submit" 
                disabled={isSubmitting}
                className="w-full sm:w-auto"
              >
                {isSubmitting ? "Processing..." : "Run Analysis"}
              </Button>
            </div>
          </form>
        </div>
      </FormProvider>
    </TooltipProvider>
  );
}

