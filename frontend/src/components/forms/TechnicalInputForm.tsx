"use client";

import React, { useEffect } from "react";
import { useForm, FormProvider } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import * as z from "zod";
import { Button } from "@/components/ui/button";
import { TechnicalParameters } from "@/types/technical";
import { ProcessTypeEnum, ProcessType, technicalValidationSchema, TechnicalValidationData } from '@/types/process';
import { FormSection } from "./shared/FormSection";
import { FormNumberInput } from "./shared/FormNumberInput";
import { FormSelect } from "./shared/FormSelect";
import { TooltipProvider } from "@/components/ui/tooltip";
import { Progress } from "@/components/ui/progress";
import { ArrowRight, Loader2 } from "lucide-react";
import { Card } from "@/components/ui/card";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogFooter,
} from "@/components/ui/dialog";
import { DEFAULT_TECHNICAL_VALUES } from './index';

const processTypeOptions = [
  { value: ProcessTypeEnum.BASELINE, label: 'Baseline' },
  { value: ProcessTypeEnum.RF, label: 'RF' },
  { value: ProcessTypeEnum.IR, label: 'IR' }
];

type TechnicalFormValues = TechnicalValidationData;

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
  const [showProcessDialog, setShowProcessDialog] = React.useState(false);
  const form = useForm<TechnicalFormValues>({
    resolver: zodResolver(technicalValidationSchema),
    defaultValues: initialData || DEFAULT_TECHNICAL_VALUES,
    mode: "onChange"
  });

  const processType = form.watch('process_type');

  // Show process dialog for RF/IR selection
  useEffect(() => {
    if (processType !== ProcessTypeEnum.BASELINE && !initialData) {
      setShowProcessDialog(true);
    }
  }, [processType, initialData]);

  // Set process-specific parameters when process type changes
  useEffect(() => {
    if (processType === ProcessTypeEnum.BASELINE) {
      form.setValue('electricity_consumption', undefined);
      form.setValue('cooling_consumption', undefined);
      form.setValue('water_consumption', 0.2);
    } else if (processType === ProcessTypeEnum.RF) {
      form.setValue('cooling_consumption', undefined);
      form.setValue('electricity_consumption', 0.75);
      form.setValue('water_consumption', 0.15);
    } else if (processType === ProcessTypeEnum.IR) {
      form.setValue('electricity_consumption', undefined);
      form.setValue('cooling_consumption', 0.45);
      form.setValue('water_consumption', 0.25);
    }
  }, [processType, form]);

  const getRequiredFields = () => {
    const fields = [
      'process_type', 'air_flow', 'classifier_speed', 'input_mass', 'output_mass',
      'initial_protein_content', 'final_protein_content', 'initial_moisture_content',
      'final_moisture_content', 'd10_particle_size', 'd50_particle_size', 'd90_particle_size'
    ];

    if (processType === ProcessTypeEnum.RF) {
      return [...fields, 'electricity_consumption', 'water_consumption'];
    } else if (processType === ProcessTypeEnum.IR) {
      return [...fields, 'cooling_consumption', 'water_consumption'];
    }
    return fields;
  };

  const calculateProgress = () => {
    const fields = getRequiredFields();
    const values = form.getValues();
    const filledFields = fields.filter(field => {
      const value = values[field as keyof TechnicalFormValues];
      return value !== undefined && value !== null && !form.formState.errors[field as keyof TechnicalFormValues];
    });
    return (filledFields.length / fields.length) * 100;
  };

  const progress = calculateProgress();

  const handleProcessParametersSubmit = async () => {
    // Trigger validation for the specific fields
    const result = await form.trigger([
      'electricity_consumption',
      'cooling_consumption',
      'water_consumption'
    ]);

    if (result) {
      setShowProcessDialog(false);
    }
  };

  // Add this function to handle dialog close attempts
  const handleDialogClose = (open: boolean) => {
    if (!open) {
      // If trying to close, validate first
      handleProcessParametersSubmit();
    }
  };

  const handleFormSubmit = async (data: TechnicalFormValues) => {
    // Basic parameters
    if (!data.process_type) {
      form.setError('process_type', {
        type: 'manual',
        message: 'Process type is required'
      });
      return;
    }

    // Validate all required fields
    const requiredFields = getRequiredFields();
    const missingFields = requiredFields.filter(field => {
      const value = data[field as keyof TechnicalFormValues];
      return value === undefined || value === null;
    });

    if (missingFields.length > 0) {
      missingFields.forEach(field => {
        form.setError(field as any, {
          type: 'manual',
          message: `${field} is required`
        });
      });
      return;
    }

    // Process type specific validation
    if (data.process_type === ProcessTypeEnum.RF) {
      if (!data.electricity_consumption || !data.water_consumption) {
        if (!data.electricity_consumption) {
          form.setError('electricity_consumption', {
            type: 'manual',
            message: 'Electricity consumption is required for RF process'
          });
        }
        if (!data.water_consumption) {
          form.setError('water_consumption', {
            type: 'manual',
            message: 'Water consumption is required for RF process'
          });
        }
        return;
      }
    }

    if (data.process_type === ProcessTypeEnum.IR) {
      if (!data.cooling_consumption || !data.water_consumption) {
        if (!data.cooling_consumption) {
          form.setError('cooling_consumption', {
            type: 'manual',
            message: 'Cooling consumption is required for IR process'
          });
        }
        if (!data.water_consumption) {
          form.setError('water_consumption', {
            type: 'manual',
            message: 'Water consumption is required for IR process'
          });
        }
        return;
      }
    }

    // If all validations pass, submit the data
    onSubmit(data);
  };

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

          <form id="technical-form" onSubmit={form.handleSubmit(handleFormSubmit)} className="space-y-8">
            <div className="grid gap-6">
              <Card className="p-6">
                <FormSection 
                  title="Process Parameters" 
                  tooltip="Configure the main process parameters for the separation process"
                >
                  <div className="grid gap-4 sm:grid-cols-2">
                    <FormSelect
                      name="process_type"
                      label="Process Type"
                      options={processTypeOptions}
                      required
                      tooltip="Select the type of separation process to analyze"
                    />
                    <FormNumberInput
                      name="air_flow"
                      label="Air Flow Rate"
                      unit="m³/h"
                      min={0}
                      max={1000}
                      required
                      tooltip="The volumetric flow rate of air through the system"
                    />
                    <FormNumberInput
                      name="classifier_speed"
                      label="Classifier Speed"
                      unit="rpm"
                      min={0}
                      required
                      tooltip="The rotational speed of the classifier wheel"
                    />
                    {/* Process-specific parameters */}
                    {processType === ProcessTypeEnum.RF && (
                      <FormNumberInput
                        name="electricity_consumption"
                        label="Electricity Consumption"
                        unit="kWh/kg"
                        min={0}
                        step={0.01}
                        required
                        tooltip="Specific electricity consumption per kg of product"
                      />
                    )}
                    {processType === ProcessTypeEnum.IR && (
                      <FormNumberInput
                        name="cooling_consumption"
                        label="Cooling Consumption"
                        unit="kWh/kg"
                        min={0}
                        step={0.01}
                        required
                        tooltip="Specific cooling energy consumption per kg of product"
                      />
                    )}
                    <FormNumberInput
                      name="water_consumption"
                      label="Water Consumption"
                      unit="m³/kg"
                      min={0}
                      step={0.001}
                      required
                      tooltip="Specific water consumption per kg of product"
                    />
                  </div>
                </FormSection>
              </Card>

              <Dialog open={showProcessDialog} onOpenChange={handleDialogClose}>
                <DialogContent>
                  <DialogHeader>
                    <DialogTitle>{processType.toUpperCase()} Process Parameters</DialogTitle>
                    <DialogDescription>
                      Please configure the specific parameters for {processType.toUpperCase()} process type.
                      These parameters are required before proceeding.
                    </DialogDescription>
                  </DialogHeader>
                  <form onSubmit={(e) => { e.preventDefault(); handleProcessParametersSubmit(); }}>
                    <div className="grid gap-4 py-4">
                      {processType === ProcessTypeEnum.RF && (
                        <FormNumberInput
                          name="electricity_consumption"
                          label="Electricity Consumption"
                          unit="kWh"
                          min={0}
                          required
                          tooltip="Electricity consumption for RF process"
                        />
                      )}
                      {processType === ProcessTypeEnum.IR && (
                        <FormNumberInput
                          name="cooling_consumption"
                          label="Cooling Consumption"
                          unit="kWh"
                          min={0}
                          required
                          tooltip="Cooling consumption for IR process"
                        />
                      )}
                      <FormNumberInput
                        name="water_consumption"
                        label="Water Consumption"
                        unit="m³"
                        min={0}
                        required
                        tooltip="Water consumption for the process"
                      />
                    </div>
                    <DialogFooter>
                      <Button type="submit">
                        Continue
                      </Button>
                    </DialogFooter>
                  </form>
                </DialogContent>
              </Dialog>

              <Card className="p-6">
                <FormSection 
                  title="Mass Balance" 
                  tooltip="Input the mass flow parameters for the process"
                >
                  <div className="grid gap-4 sm:grid-cols-2">
                    <FormNumberInput
                      name="input_mass"
                      label="Input Mass"
                      unit="kg"
                      min={0}
                      max={10000}
                      required
                      tooltip="Total mass of feed material entering the process"
                    />
                    <FormNumberInput
                      name="output_mass"
                      label="Output Mass"
                      unit="kg"
                      min={0}
                      max={10000}
                      required
                      tooltip="Total mass of product material after processing"
                    />
                  </div>
                </FormSection>
              </Card>

              <Card className="p-6">
                <FormSection 
                  title="Content Analysis" 
                  tooltip="Specify the protein and moisture content before and after processing"
                >
                  <div className="grid gap-4 sm:grid-cols-2">
                    <FormNumberInput
                      name="initial_protein_content"
                      label="Initial Protein Content"
                      unit="%"
                      min={0}
                      max={100}
                      required
                      tooltip="Protein content in the feed material"
                    />
                    <FormNumberInput
                      name="final_protein_content"
                      label="Final Protein Content"
                      unit="%"
                      min={0}
                      max={100}
                      required
                      tooltip="Protein content in the product material"
                    />
                    <FormNumberInput
                      name="initial_moisture_content"
                      label="Initial Moisture Content"
                      unit="%"
                      min={0}
                      max={100}
                      required
                      tooltip="Moisture content in the feed material"
                    />
                    <FormNumberInput
                      name="final_moisture_content"
                      label="Final Moisture Content"
                      unit="%"
                      min={0}
                      max={100}
                      required
                      tooltip="Moisture content in the product material"
                    />
                  </div>
                </FormSection>
              </Card>

              <Card className="p-6">
                <FormSection 
                  title="Particle Size Analysis" 
                  tooltip="Enter the particle size distribution parameters"
                >
                  <div className="grid gap-4 sm:grid-cols-2">
                    <FormNumberInput
                      name="d10_particle_size"
                      label="D10 Particle Size"
                      unit="μm"
                      min={0}
                      required
                      tooltip="Particle size at which 10% of the sample is comprised of smaller particles"
                    />
                    <FormNumberInput
                      name="d50_particle_size"
                      label="D50 Particle Size"
                      unit="μm"
                      min={0}
                      required
                      tooltip="Median particle size (50% of particles are smaller)"
                    />
                    <FormNumberInput
                      name="d90_particle_size"
                      label="D90 Particle Size"
                      unit="μm"
                      min={0}
                      required
                      tooltip="Particle size at which 90% of the sample is comprised of smaller particles"
                    />
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
