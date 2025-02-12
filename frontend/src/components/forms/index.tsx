"use client"

import React, { useState } from 'react';
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import * as z from "zod";
import { Button } from "@/components/ui/button";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { ProcessType } from '@/types/process';
import { DEFAULT_PROCESS_ANALYSIS } from '@/config/constants';
import TechnicalInputForm from './TechnicalInputForm';
import EconomicInputForm from './EconomicInputForm';
import EnvironmentalInputForm from './EnvironmentalInputForm';
import { PROCESS_ENDPOINTS, API_CONFIG } from '@/config/endpoints';
import axios from 'axios';
import { EnvironmentalParameters } from '@/types/environmental';
import { Steps } from "@/components/ui/steps";
import { Card, CardContent } from "@/components/ui/card";
import { useToast } from "@/hooks/useToast";

const processSchema = z.object({
  type: z.enum(["technical", "economic", "environmental"] as const),
  parameters: z.object({
    // Technical parameters
    processType: z.enum(["batch", "continuous"]).optional(),
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
    equipmentCost: z.number().optional(),
    maintenanceCost: z.number().optional(),
    rawMaterialCost: z.number().optional(),
    utilityCost: z.number().optional(),
    laborCost: z.number().optional(),
    projectDuration: z.number().optional(),
    discountRate: z.number().optional(),
    productionVolume: z.number().optional(),
    revenuePerYear: z.number().optional(),
    
    // Environmental parameters
    electricityConsumption: z.number().optional(),
    coolingConsumption: z.number().optional(),
    waterConsumption: z.number().optional(),
    transportConsumption: z.number().optional(),
    equipmentMass: z.number().optional(),
    allocationMethod: z.string().optional(),
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
  parameters: {}
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
        'parameters.equipmentCost',
        'parameters.maintenanceCost',
        'parameters.rawMaterialCost',
        'parameters.utilityCost',
        'parameters.laborCost',
        'parameters.projectDuration',
        'parameters.discountRate',
        'parameters.productionVolume',
        'parameters.revenuePerYear'
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
        'parameters.electricityConsumption',
        'parameters.coolingConsumption',
        'parameters.waterConsumption',
        'parameters.transportConsumption',
        'parameters.equipmentMass',
        'parameters.allocationMethod'
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
    const { electricityConsumption, coolingConsumption, processType } = values.parameters;

    if (processType === "batch" && !electricityConsumption) {
      errors.push('Batch process requires electricity consumption');
    }
    if (processType === "continuous" && !coolingConsumption) {
      errors.push('Continuous process requires cooling consumption');
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
