"use client";

import React from "react";
import { useForm, FormProvider } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { EnvironmentalParameters } from "@/types/environmental";
import { FormSection } from "./shared/FormSection";
import { FormNumberInput } from "./shared/FormNumberInput";
import { FormSelect } from "./shared/FormSelect";
import { TooltipProvider } from "@/components/ui/tooltip";
import { Progress } from "@/components/ui/progress";
import { ArrowRight, Loader2 } from "lucide-react";
import { Card } from "@/components/ui/card";
import { environmentalValidationSchema, EnvironmentalValidationData } from '@/types/process';
import { DEFAULT_ENVIRONMENTAL_VALUES } from './index';

const allocationMethodOptions = [
  { value: 'economic', label: 'Economic Allocation' },
  { value: 'physical', label: 'Physical Allocation' },
  { value: 'hybrid', label: 'Hybrid Allocation' }
];

type EnvironmentalFormValues = EnvironmentalValidationData;

interface EnvironmentalInputFormProps {
  onSubmit: (values: EnvironmentalParameters) => void;
  isSubmitting?: boolean;
  initialData?: EnvironmentalParameters;
}

export default function EnvironmentalInputForm({
  onSubmit,
  isSubmitting = false,
  initialData
}: EnvironmentalInputFormProps) {
  const form = useForm<EnvironmentalFormValues>({
    resolver: zodResolver(environmentalValidationSchema),
    defaultValues: initialData || DEFAULT_ENVIRONMENTAL_VALUES,
    mode: "onChange"
  });

  const watchAllocationMethod = form.watch("allocation_method");

  const getRequiredFields = () => {
    const fields = [
      'production_volume', 'electricity_consumption', 'water_consumption',
      'equipment_mass', 'thermal_ratio', 'allocation_method'
    ];
    
    if (form.watch('allocation_method') === 'hybrid') {
      fields.push('hybrid_weights.economic', 'hybrid_weights.physical');
    }
    
    return fields;
  };

  const calculateProgress = () => {
    const fields = getRequiredFields();
    const values = form.getValues();
    const filledFields = fields.filter(field => {
      let value;
      if (field.includes('.')) {
        const [parent, child] = field.split('.');
        if (parent === 'hybrid_weights') {
          value = (values.hybrid_weights as Record<string, number>)?.[child];
        }
      } else {
        value = values[field as keyof EnvironmentalFormValues];
      }
      return value !== undefined && value !== null && !form.formState.errors[field as keyof EnvironmentalFormValues];
    });
    return (filledFields.length / fields.length) * 100;
  };

  const progress = calculateProgress();

  const handleFormSubmit = async (data: EnvironmentalFormValues) => {
    // Basic parameters
    if (!data.production_volume || data.production_volume <= 0) {
      form.setError('production_volume', {
        type: 'manual',
        message: 'Production volume must be positive'
      });
      return;
    }
    if (!data.equipment_mass || data.equipment_mass <= 0) {
      form.setError('equipment_mass', {
        type: 'manual',
        message: 'Equipment mass must be positive'
      });
      return;
    }

    // Resource consumption
    if (!data.electricity_consumption || data.electricity_consumption <= 0) {
      form.setError('electricity_consumption', {
        type: 'manual',
        message: 'Electricity consumption must be positive'
      });
      return;
    }
    if (!data.water_consumption || data.water_consumption <= 0) {
      form.setError('water_consumption', {
        type: 'manual',
        message: 'Water consumption must be positive'
      });
      return;
    }
    if (data.cooling_consumption < 0) {
      form.setError('cooling_consumption', {
        type: 'manual',
        message: 'Cooling consumption cannot be negative'
      });
      return;
    }
    if (data.transport_consumption < 0) {
      form.setError('transport_consumption', {
        type: 'manual',
        message: 'Transport consumption cannot be negative'
      });
      return;
    }

    // Process efficiency
    if (!data.thermal_ratio || data.thermal_ratio < 0 || data.thermal_ratio > 1) {
      form.setError('thermal_ratio', {
        type: 'manual',
        message: 'Thermal ratio must be between 0 and 1'
      });
      return;
    }

    // Allocation configuration
    if (!data.allocation_method || !['economic', 'physical', 'hybrid'].includes(data.allocation_method)) {
      form.setError('allocation_method', {
        type: 'manual',
        message: 'Please select a valid allocation method'
      });
      return;
    }

    // Hybrid allocation validation
    if (data.allocation_method === 'hybrid') {
      const weights = data.hybrid_weights || {};
      const totalWeight = (weights.economic || 0) + (weights.physical || 0);
      if (Math.abs(totalWeight - 1) > 0.001) {
        form.setError('hybrid_weights.economic', {
          type: 'manual',
          message: 'Hybrid weights must sum to 1'
        });
        return;
      }
    }

    onSubmit(data);
  };

  return (
    <TooltipProvider>
      <FormProvider {...form}>
        <div className="space-y-6 max-w-4xl mx-auto">
          <div className="space-y-2 mb-8">
            <div className="flex justify-between items-center">
              <h2 className="text-lg font-semibold">Environmental Analysis Parameters</h2>
              <span className="text-sm text-muted-foreground">
                {Math.round(progress)}% Complete
              </span>
            </div>
            <Progress value={progress} className="h-2" />
          </div>

          <form id="environmental-form" onSubmit={form.handleSubmit(handleFormSubmit)} className="space-y-8">
            <div className="grid gap-6">
              <Card className="p-6">
                <FormSection 
                  title="Process Configuration" 
                  tooltip="Configure the basic process parameters"
                >
                  <div className="grid gap-4 sm:grid-cols-2">
                    <FormNumberInput
                      name="production_volume"
                      label="Production Volume"
                      unit="kg/year"
                      min={0}
                      required
                      tooltip="Annual production capacity"
                    />
                    <FormNumberInput
                      name="equipment_mass"
                      label="Equipment Mass"
                      unit="kg"
                      min={0}
                      required
                      tooltip="Total mass of process equipment"
                    />
                  </div>
                </FormSection>
              </Card>

              <Card className="p-6">
                <FormSection 
                  title="Resource Consumption" 
                  tooltip="Specify the resource consumption parameters"
                >
                  <div className="grid gap-4 sm:grid-cols-2">
                    <FormNumberInput
                      name="electricity_consumption"
                      label="Electricity Consumption"
                      unit="kWh/kg"
                      min={0}
                      step={0.01}
                      required
                      tooltip="Specific electricity consumption per kg of product"
                    />
                    <FormNumberInput
                      name="water_consumption"
                      label="Water Consumption"
                      unit="kg"
                      min={0}
                      required
                      tooltip="Total water consumption"
                    />
                    <FormNumberInput
                      name="cooling_consumption"
                      label="Cooling Consumption"
                      unit="kWh/kg"
                      min={0}
                      step={0.01}
                      required
                      tooltip="Specific cooling energy consumption per kg of product"
                    />
                    <FormNumberInput
                      name="transport_consumption"
                      label="Transport Energy"
                      unit="MJ"
                      min={0}
                      required
                      tooltip="Transport energy consumption"
                    />
                  </div>
                </FormSection>
              </Card>

              <Card className="p-6">
                <FormSection 
                  title="Process Efficiency" 
                  tooltip="Configure process efficiency parameters"
                >
                  <div className="grid gap-4 sm:grid-cols-2">
                    <FormNumberInput
                      name="thermal_ratio"
                      label="Thermal Ratio"
                      unit="ratio"
                      min={0}
                      max={1}
                      step={0.01}
                      required
                      tooltip="Ratio of thermal to electrical energy consumption"
                    />
                  </div>
                </FormSection>
              </Card>

              <Card className="p-6">
                <FormSection 
                  title="Impact Allocation" 
                  tooltip="Configure how environmental impacts are allocated"
                >
                  <div className="grid gap-4 sm:grid-cols-2">
                    <FormSelect
                      name="allocation_method"
                      label="Allocation Method"
                      options={allocationMethodOptions}
                      required
                      tooltip="Method for allocating environmental impacts between products"
                    />
                    {watchAllocationMethod === 'hybrid' && (
                      <>
                        <FormNumberInput
                          name="hybrid_weights.economic"
                          label="Economic Weight"
                          unit="ratio"
                          min={0}
                          max={1}
                          step={0.01}
                          required
                          tooltip="Weight for economic allocation in hybrid method"
                        />
                        <FormNumberInput
                          name="hybrid_weights.physical"
                          label="Physical Weight"
                          unit="ratio"
                          min={0}
                          max={1}
                          step={0.01}
                          required
                          tooltip="Weight for physical allocation in hybrid method"
                        />
                      </>
                    )}
                  </div>
                </FormSection>
              </Card>
            </div>
          </form>
        </div>
      </FormProvider>
    </TooltipProvider>
  );
}
