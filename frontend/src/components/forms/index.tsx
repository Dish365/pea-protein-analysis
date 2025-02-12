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

const processSchema = z.object({
  type: z.enum(["technical", "economic", "environmental"] as const),
  parameters: z.object({
    // Technical parameters
    processType: z.enum(["baseline", "rf", "ir"] as const),
    airFlow: z.number().optional(),
    classifierSpeed: z.number().optional(),
    inputMass: z.number().optional(),
    outputMass: z.number().optional(),
    initialProteinContent: z.number().optional(),
    finalProteinContent: z.number().optional(),
    initialMoistureContent: z.number().optional(),
    finalMoistureContent: z.number().optional(),
    d10ParticleSize: z.number().optional(),
    d50ParticleSize: z.number().optional(),
    d90ParticleSize: z.number().optional(),
    
    // Economic parameters
    production_volume: z.number().optional(),
    operating_hours: z.number().optional(),
    equipment_cost: z.number().optional(),
    utility_cost: z.number().optional(),
    raw_material_cost: z.number().optional(),
    labor_cost: z.number().optional(),
    maintenance_factor: z.number().optional(),
    indirect_costs_factor: z.number().optional(),
    installation_factor: z.number().optional(),
    project_duration: z.number().optional(),
    discount_rate: z.number().optional(),
    revenue_per_year: z.number().optional(),
    
    // Environmental parameters
    electricity_consumption: z.number().optional(),
    cooling_consumption: z.number().optional(),
    water_consumption: z.number().optional(),
    transport_consumption: z.number().optional(),
    equipment_mass: z.number().optional(),
    thermal_ratio: z.number().optional(),
    allocation_method: z.enum(["economic", "physical", "hybrid"]).optional(),
    hybrid_weights: z.record(z.string(), z.number()).optional(),
  }),
});

export type ProcessAnalysis = z.infer<typeof processSchema>;

interface ProcessInputFormProps {
  onSubmit?: (values: ProcessAnalysis) => void;
  onSuccess?: (response: any) => void;
  initialValues?: Partial<ProcessAnalysis>;
  loading?: boolean;
}

interface FormStep {
  title: string;
  description: string;
  validateFields: string[];
  component: React.ReactNode;
}

const DEFAULT_FORM_VALUES: ProcessAnalysis = {
  type: "technical",
  parameters: {
    processType: "baseline",
  }
};

const ProcessInputForm: React.FC<ProcessInputFormProps> = ({
  onSubmit,
  onSuccess,
  initialValues = DEFAULT_FORM_VALUES,
  loading: externalLoading = false,
}) => {
  const form = useForm<ProcessAnalysis>({
    resolver: zodResolver(processSchema),
    defaultValues: {
      type: initialValues?.type || "technical",
      parameters: initialValues?.parameters || {},
    },
  });
  const [currentStep, setCurrentStep] = useState(1);
  const { toast } = useToast();

  const steps: FormStep[] = [
    {
      title: 'Technical Parameters',
      description: 'Configure process specifications',
      validateFields: [
        'parameters.processType',
        'parameters.airFlow',
        'parameters.classifierSpeed',
        'parameters.inputMass',
        'parameters.outputMass',
        'parameters.initialProteinContent',
        'parameters.finalProteinContent',
        'parameters.initialMoistureContent',
        'parameters.finalMoistureContent',
        'parameters.d10ParticleSize',
        'parameters.d50ParticleSize',
        'parameters.d90ParticleSize',
      ],
      component: (
        <TechnicalInputForm 
          onSubmit={async (technicalValues) => {
            form.setValue('parameters', { ...form.getValues().parameters, ...technicalValues });
            const isValid = await form.trigger(steps[currentStep - 1].validateFields as any[]);
            if (isValid) next();
          }}
          isSubmitting={form.formState.isSubmitting}
        />
      ),
    },
    {
      title: 'Economic Parameters',
      description: 'Define cost and revenue factors',
      validateFields: [
        'parameters.equipment_cost',
        'parameters.utility_cost',
        'parameters.raw_material_cost',
        'parameters.labor_cost',
        'parameters.maintenance_factor',
        'parameters.indirect_costs_factor',
        'parameters.installation_factor',
        'parameters.project_duration',
        'parameters.discount_rate',
        'parameters.revenue_per_year',
      ],
      component: (
        <EconomicInputForm 
          onSubmit={async (economicValues) => {
            form.setValue('parameters', { ...form.getValues().parameters, ...economicValues });
            const isValid = await form.trigger(steps[currentStep - 1].validateFields as any[]);
            if (isValid) next();
          }}
          isSubmitting={form.formState.isSubmitting}
        />
      ),
    },
    {
      title: 'Environmental Parameters',
      description: 'Specify environmental impacts',
      validateFields: [
        'parameters.electricity_consumption',
        'parameters.cooling_consumption',
        'parameters.water_consumption',
        'parameters.transport_consumption',
        'parameters.equipment_mass',
        'parameters.thermal_ratio',
        'parameters.allocation_method',
        'parameters.hybrid_weights',
      ],
      component: (
        <EnvironmentalInputForm 
          onSubmit={async (environmentalValues) => {
            form.setValue('parameters', { ...form.getValues().parameters, ...environmentalValues });
            const isValid = await form.trigger(steps[currentStep - 1].validateFields as any[]);
            if (isValid) handleSubmit(form.getValues());
          }}
          isSubmitting={form.formState.isSubmitting}
        />
      ),
    },
  ];

  const validateProcessTypeRequirements = (values: ProcessAnalysis) => {
    const errors: string[] = [];
    const params = values.parameters;

    if (params.processType === "rf" && !params.electricity_consumption) {
      errors.push('RF process requires electricity consumption');
    }
    if (params.processType === "ir" && !params.cooling_consumption) {
      errors.push('IR process requires cooling consumption');
    }

    return errors;
  };

  const handleSubmit = async (values: ProcessAnalysis) => {
    try {
      if (onSubmit) {
        await onSubmit(values);
      }
      if (onSuccess) {
        onSuccess(values);
      }
    } catch (error) {
      console.error("Form submission error:", error);
    }
  };

  const next = async () => {
    try {
      const isValid = await form.trigger(steps[currentStep - 1].validateFields as any[]);
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
                  Next
                </Button>
              )}
              {currentStep === steps.length && (
                <Button
                  type="submit"
                  disabled={form.formState.isSubmitting || externalLoading}
                >
                  {form.formState.isSubmitting || externalLoading ? "Starting Analysis..." : "Start Analysis"}
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
