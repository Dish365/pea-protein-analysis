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
import { ProcessTypeEnum, technicalSchema, economicSchema, environmentalSchema } from '@/types/process';

const processSchema = z.object({
  type: z.enum(["technical", "economic", "environmental"] as const),
  parameters: z.object({
    // Technical parameters
    process_type: z.nativeEnum(ProcessTypeEnum),
    air_flow: z.number().min(0).max(1000),
    classifier_speed: z.number().min(0),
    input_mass: z.number().min(0).max(10000),
    output_mass: z.number().min(0).max(10000),
    initial_protein_content: z.number().min(0).max(100),
    final_protein_content: z.number().min(0).max(100),
    initial_moisture_content: z.number().min(0).max(100),
    final_moisture_content: z.number().min(0).max(100),
    d10_particle_size: z.number().min(0),
    d50_particle_size: z.number().min(0),
    d90_particle_size: z.number().min(0),
    
    // Process-specific parameters
    electricity_consumption: z.number().min(0).optional(),
    cooling_consumption: z.number().min(0).optional(),
    water_consumption: z.number().min(0).optional(),
    
    // Economic parameters
    production_volume: z.number().min(0),
    operating_hours: z.number().min(0).max(8760),
    equipment_cost: z.number().min(0),
    utility_cost: z.number().min(0),
    raw_material_cost: z.number().min(0),
    labor_cost: z.number().min(0),
    maintenance_factor: z.number().min(0).max(1),
    indirect_costs_factor: z.number().min(0).max(1),
    installation_factor: z.number().min(0).max(1),
    project_duration: z.number().min(0),
    discount_rate: z.number().min(0).max(1),
    revenue_per_year: z.number().min(0),
    
    // Environmental parameters
    transport_consumption: z.number().min(0).optional(),
    equipment_mass: z.number().min(0).optional(),
    thermal_ratio: z.number().min(0).max(1).optional(),
    allocation_method: z.enum(['economic', 'physical', 'hybrid'] as const),
    hybrid_weights: z.record(z.string(), z.number().min(0).max(1)).optional()
  }).superRefine((data, ctx) => {
    // Technical validation
    if (data.output_mass > data.input_mass) {
      ctx.addIssue({
        code: z.ZodIssueCode.custom,
        message: "Output mass cannot exceed input mass",
        path: ["output_mass"]
      });
    }
    
    if (data.final_moisture_content > data.initial_moisture_content) {
      ctx.addIssue({
        code: z.ZodIssueCode.custom,
        message: "Final moisture content cannot be higher than initial moisture content",
        path: ["final_moisture_content"]
      });
    }
    
    if (data.d50_particle_size < data.d10_particle_size) {
      ctx.addIssue({
        code: z.ZodIssueCode.custom,
        message: "D50 must be greater than or equal to D10",
        path: ["d50_particle_size"]
      });
    }
    
    if (data.d90_particle_size < data.d50_particle_size) {
      ctx.addIssue({
        code: z.ZodIssueCode.custom,
        message: "D90 must be greater than or equal to D50",
        path: ["d90_particle_size"]
      });
    }
    
    // Process type specific validation
    if (data.process_type === ProcessTypeEnum.RF) {
      if (!data.electricity_consumption || data.electricity_consumption <= 0) {
        ctx.addIssue({
          code: z.ZodIssueCode.custom,
          message: "Electricity consumption is required for RF process",
          path: ["electricity_consumption"]
        });
      }
      if (!data.water_consumption || data.water_consumption <= 0) {
        ctx.addIssue({
          code: z.ZodIssueCode.custom,
          message: "Water consumption is required for RF process",
          path: ["water_consumption"]
        });
      }
    }
    
    if (data.process_type === ProcessTypeEnum.IR) {
      if (!data.cooling_consumption || data.cooling_consumption <= 0) {
        ctx.addIssue({
          code: z.ZodIssueCode.custom,
          message: "Cooling consumption is required for IR process",
          path: ["cooling_consumption"]
        });
      }
      if (!data.water_consumption || data.water_consumption <= 0) {
        ctx.addIssue({
          code: z.ZodIssueCode.custom,
          message: "Water consumption is required for IR process",
          path: ["water_consumption"]
        });
      }
    }
  })
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

const DEFAULT_FORM_VALUES = {
  type: "technical" as const,
  parameters: {
    process_type: ProcessTypeEnum.BASELINE,
    air_flow: 0,
    classifier_speed: 0,
    input_mass: 0,
    output_mass: 0,
    initial_protein_content: 0,
    final_protein_content: 0,
    initial_moisture_content: 0,
    final_moisture_content: 0,
    d10_particle_size: 0,
    d50_particle_size: 0,
    d90_particle_size: 0,
    production_volume: 0,
    operating_hours: 0,
    equipment_cost: 0,
    utility_cost: 0,
    raw_material_cost: 0,
    labor_cost: 0,
    maintenance_factor: 0,
    indirect_costs_factor: 0,
    installation_factor: 0,
    project_duration: 0,
    discount_rate: 0,
    revenue_per_year: 0,
    allocation_method: 'economic' as const
  }
} satisfies z.infer<typeof processSchema>;

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
        'parameters.process_type',
        'parameters.air_flow',
        'parameters.classifier_speed',
        'parameters.input_mass',
        'parameters.output_mass',
        'parameters.initial_protein_content',
        'parameters.final_protein_content',
        'parameters.initial_moisture_content',
        'parameters.final_moisture_content',
        'parameters.d10_particle_size',
        'parameters.d50_particle_size',
        'parameters.d90_particle_size',
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
        'parameters.production_volume',
        'parameters.operating_hours',
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

  const handleSubmit = async (values: ProcessAnalysis) => {
    try {
      // Only submit when all steps are completed
      if (currentStep === steps.length) {
        const params = values.parameters;
        
        // Validate technical parameters
        const technicalFields = [
          'process_type', 'air_flow', 'classifier_speed', 'input_mass', 'output_mass',
          'initial_protein_content', 'final_protein_content', 'initial_moisture_content',
          'final_moisture_content', 'd10_particle_size', 'd50_particle_size', 'd90_particle_size'
        ];
        
        const missingTechnical = technicalFields.filter(field => !params[field as keyof typeof params]);
        if (missingTechnical.length > 0) {
          toast({
            title: "Technical Validation Error",
            description: `Missing required technical parameters: ${missingTechnical.join(', ')}`,
            variant: "destructive",
          });
          return;
        }

        // Validate process-specific requirements
        if (params.process_type === ProcessTypeEnum.RF && (!params.electricity_consumption || !params.water_consumption)) {
          toast({
            title: "Technical Validation Error",
            description: "RF process requires electricity and water consumption parameters",
            variant: "destructive",
          });
          return;
        }
        if (params.process_type === ProcessTypeEnum.IR && (!params.cooling_consumption || !params.water_consumption)) {
          toast({
            title: "Technical Validation Error",
            description: "IR process requires cooling and water consumption parameters",
            variant: "destructive",
          });
          return;
        }

        // Validate economic parameters
        const economicFields = [
          'production_volume', 'operating_hours', 'equipment_cost', 'utility_cost',
          'raw_material_cost', 'labor_cost', 'maintenance_factor', 'indirect_costs_factor',
          'installation_factor', 'project_duration', 'discount_rate', 'revenue_per_year'
        ];
        
        const missingEconomic = economicFields.filter(field => !params[field as keyof typeof params]);
        if (missingEconomic.length > 0) {
          toast({
            title: "Economic Validation Error",
            description: `Missing required economic parameters: ${missingEconomic.join(', ')}`,
            variant: "destructive",
          });
          return;
        }

        // Validate environmental parameters
        const environmentalFields = [
          'electricity_consumption', 'water_consumption', 'equipment_mass',
          'thermal_ratio', 'allocation_method'
        ];
        
        const missingEnvironmental = environmentalFields.filter(field => !params[field as keyof typeof params]);
        if (missingEnvironmental.length > 0) {
          toast({
            title: "Environmental Validation Error",
            description: `Missing required environmental parameters: ${missingEnvironmental.join(', ')}`,
            variant: "destructive",
          });
          return;
        }

        // Validate hybrid allocation if selected
        if (params.allocation_method === 'hybrid') {
          const weights = params.hybrid_weights || {};
          if (!weights.economic || !weights.physical || 
              Math.abs((weights.economic + weights.physical) - 1) > 0.001) {
            toast({
              title: "Environmental Validation Error",
              description: "Hybrid allocation weights must be provided and sum to 1",
              variant: "destructive",
            });
            return;
          }
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
      const isValid = await form.trigger(steps[currentStep - 1].validateFields as any[]);
      if (isValid) {
        // Just move to next step without submitting
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
