"use client"

import React, { useState } from 'react';
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import * as z from "zod";
import { Button } from "@/components/ui/button";
import {
  Form
} from "@/components/ui/form";
import TechnicalInputForm from './TechnicalInputForm';
import EconomicInputForm from './EconomicInputForm';
import EnvironmentalInputForm from './EnvironmentalInputForm';
import { Steps } from "@/components/ui/steps";
import { Card, CardContent } from "@/components/ui/card";
import { useToast } from "@/hooks/useToast";
import {
  ProcessTypeEnum,
  processValidationSchema,
  TechnicalValidationData,
  EconomicValidationData,
  EnvironmentalValidationData,
  validateProcessData
} from '@/types/process';

// Define the form's data structure to match our validation schema
interface ProcessFormData {
  technical: TechnicalValidationData;
  economic: EconomicValidationData;
  environmental: EnvironmentalValidationData;
}

interface ProcessInputFormProps {
  onSubmit?: (values: ProcessFormData) => void;
  onSuccess?: (response: any) => void;
  initialValues?: Partial<ProcessFormData>;
  loading?: boolean;
}

interface FormStep {
  title: string;
  description: string;
  component: React.ReactNode;
}

export const DEFAULT_TECHNICAL_VALUES = {
  process_type: ProcessTypeEnum.BASELINE,
  air_flow: 100,
  classifier_speed: 1000,
  input_mass: 1000,
  output_mass: 800,
  initial_protein_content: 80,
  final_protein_content: 45,
  initial_moisture_content: 12,
  final_moisture_content: 8,
  d10_particle_size: 10,
  d50_particle_size: 50,
  d90_particle_size: 90,
  electricity_consumption: 0.5,
  cooling_consumption: 0.3,
  water_consumption: 0.2,
  transport_consumption: 0.4,
  equipment_mass: 1000,
  thermal_ratio: 0.3
} as const;

export const DEFAULT_ECONOMIC_VALUES: EconomicValidationData = {
  // Production Parameters
  production_volume: 1000,
  operating_hours: 2000,

  // Equipment Configuration
  equipment: [{
    name: "main_equipment",
    cost: 50000,
    efficiency: 0.85,
    maintenance_cost: 2500,
    energy_consumption: 100,
    processing_capacity: 1000
  }],
  equipment_cost: 50000,
  maintenance_cost: 2500,
  installation_factor: 0.2,
  indirect_costs_factor: 0.15,
  maintenance_factor: 0.05,
  indirect_factors: [{
    name: "engineering",
    cost: 50000,
    percentage: 0.15
  }],

  // Resource Configuration
  utilities: [{
    name: "electricity",
    consumption: 100,
    unit_price: 0.15,
    unit: "kWh"
  }],
  raw_materials: [{
    name: "feed_material",
    quantity: 1000,
    unit_price: 2.5,
    unit: "kg"
  }],
  labor_config: {
    hourly_wage: 25,
    hours_per_week: 40,
    weeks_per_year: 52,
    num_workers: 1
  },

  // Operating Costs
  utility_cost: 0.15,
  raw_material_cost: 2.5,
  labor_cost: 25,

  // Financial Parameters
  project_duration: 10,
  discount_rate: 0.1,
  revenue_per_year: 100000,
  cash_flows: []
};

export const DEFAULT_ENVIRONMENTAL_VALUES: EnvironmentalValidationData = {
  production_volume: 1000,
  electricity_consumption: 0.5,
  water_consumption: 0.2,
  cooling_consumption: 0.3,
  transport_consumption: 0.4,
  equipment_mass: 1000,
  thermal_ratio: 0.3,
  allocation_method: "hybrid",
  hybrid_weights: {
    economic: 0.5,
    physical: 0.5
  }
};

const DEFAULT_FORM_VALUES: ProcessFormData = {
  technical: DEFAULT_TECHNICAL_VALUES,
  economic: DEFAULT_ECONOMIC_VALUES,
  environmental: DEFAULT_ENVIRONMENTAL_VALUES
};

const ProcessInputForm: React.FC<ProcessInputFormProps> = ({
  onSubmit,
  onSuccess,
  initialValues = DEFAULT_FORM_VALUES,
  loading: externalLoading = false,
}) => {
  const form = useForm<ProcessFormData>({
    resolver: zodResolver(processValidationSchema),
    defaultValues: initialValues,
  });
  
  const [currentStep, setCurrentStep] = useState(1);
  const { toast } = useToast();

  const steps: FormStep[] = [
    {
      title: 'Technical Parameters',
      description: 'Configure process specifications',
      component: (
        <TechnicalInputForm 
          onSubmit={async (technicalValues) => {
            form.setValue('technical', technicalValues);
            const isValid = await form.trigger('technical');
            if (isValid) next();
          }}
          isSubmitting={form.formState.isSubmitting}
          initialData={form.getValues().technical}
        />
      ),
    },
    {
      title: 'Economic Parameters',
      description: 'Define cost and revenue factors',
      component: (
        <EconomicInputForm 
          onSubmit={async (economicValues) => {
            form.setValue('economic', economicValues);
            const isValid = await form.trigger('economic');
            if (isValid) next();
          }}
          isSubmitting={form.formState.isSubmitting}
          initialData={form.getValues().economic}
        />
      ),
    },
    {
      title: 'Environmental Parameters',
      description: 'Specify environmental impacts',
      component: (
        <EnvironmentalInputForm 
          onSubmit={async (environmentalValues) => {
            form.setValue('environmental', environmentalValues);
            const isValid = await form.trigger('environmental');
            if (isValid) handleSubmit(form.getValues());
          }}
          isSubmitting={form.formState.isSubmitting}
          initialData={form.getValues().environmental}
        />
      ),
    },
  ];

  const handleSubmit = async (values: ProcessFormData) => {
    try {
      // Only submit when all steps are completed
      if (currentStep === steps.length) {
        // Validate complete process data
        const errors = validateProcessData(values);
        if (errors.length > 0) {
          errors.forEach(error => {
            toast({
              title: "Validation Error",
              description: error,
              variant: "destructive",
            });
          });
          return;
        }

        // If all validations pass, submit the data
        if (onSubmit) {
          await onSubmit(values);
        }
        if (onSuccess) {
          onSuccess(values);
        }
      }
    } catch (error) {
      console.error("Form submission error:", error);
      toast({
        title: "Error",
        description: "Failed to submit analysis. Please try again.",
        variant: "destructive",
      });
    }
  };

  const next = async () => {
    try {
      const currentStepName = ['technical', 'economic', 'environmental'][currentStep - 1];
      const isValid = await form.trigger(currentStepName as keyof ProcessFormData);
      if (isValid) {
        setCurrentStep(currentStep + 1);
      } else {
        toast({
          title: "Error",
          description: "Please fill in all required fields correctly",
          variant: "destructive",
        });
      }
    } catch (error) {
      console.error('Validation failed:', error);
      toast({
        title: "Error",
        description: "Please fill in all required fields correctly",
        variant: "destructive",
      });
    }
  };

  const prev = () => {
    setCurrentStep(currentStep - 1);
  };

  return (
    <Card className="max-w-4xl mx-auto">
      <CardContent className="pt-6">
        <Steps
          steps={steps}
          currentStep={currentStep}
        />

        <Form {...form}>
          <form onSubmit={form.handleSubmit(handleSubmit)} className="space-y-8">
            <div className="steps-content mb-8">
              {steps[currentStep - 1].component}
            </div>

            <div className="flex justify-between mt-8">
              {currentStep > 1 && (
                <Button
                  variant="outline"
                  onClick={prev}
                  disabled={form.formState.isSubmitting || externalLoading}
                >
                  Previous
                </Button>
              )}
              {currentStep < steps.length && (
                <Button
                  onClick={next}
                  disabled={form.formState.isSubmitting || externalLoading}
                >
                  Continue
                </Button>
              )}
              {currentStep === steps.length && (
                <Button
                  type="submit"
                  disabled={form.formState.isSubmitting || externalLoading}
                >
                  {form.formState.isSubmitting || externalLoading ? "Processing..." : "Complete Analysis"}
                </Button>
              )}
            </div>
          </form>
        </Form>
      </CardContent>
    </Card>
  );
};

export default ProcessInputForm;
