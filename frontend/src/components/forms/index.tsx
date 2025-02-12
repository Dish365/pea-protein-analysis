"use client"

import React, { useState } from 'react';
import { Form } from 'antd';
import { ProcessAnalysis, ProcessType } from '@/types/process';
import { DEFAULT_PROCESS_ANALYSIS } from '@/config/constants';
import TechnicalInputForm from './TechnicalInputForm';
import EconomicInputForm from './EconomicInputForm';
import EnvironmentalInputForm from './EnvironmentalInputForm';
import { PROCESS_ENDPOINTS, API_CONFIG } from '@/config/endpoints';
import axios from 'axios';
import { EnvironmentalParameters } from '@/types/environmental';
import { Steps } from "@/components/ui/steps";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { useToast } from "@/hooks/useToast";

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

const ProcessInputForm: React.FC<ProcessInputFormProps> = ({
  onSubmit,
  onSuccess,
  initialValues = DEFAULT_PROCESS_ANALYSIS,
  loading: externalLoading = false,
}) => {
  const [form] = Form.useForm();
  const [currentStep, setCurrentStep] = useState(1);
  const [loading, setLoading] = useState(false);
  const { toast } = useToast();

  const steps: FormStep[] = [
    {
      title: 'Technical Parameters',
      description: 'Configure process specifications',
      validateFields: [
        'process_type',
        'air_flow',
        'classifier_speed',
        'input_mass',
        'output_mass',
        'initial_protein_content',
        'final_protein_content',
        'initial_moisture_content',
        'final_moisture_content',
        'd10_particle_size',
        'd50_particle_size',
        'd90_particle_size',
      ],
      component: (
        <TechnicalInputForm 
          form={form}
          onSubmit={async (values) => {
            await form.validateFields();
            next();
          }}
          isSubmitting={loading}
          initialValues={initialValues}
        />
      ),
    },
    {
      title: 'Economic Parameters',
      description: 'Define cost and revenue factors',
      validateFields: [
        'equipment_cost',
        'maintenance_cost',
        'raw_material_cost',
        'utility_cost',
        'labor_cost',
        'project_duration',
        'discount_rate',
        'production_volume',
        'revenue_per_year'
      ],
      component: (
        <EconomicInputForm 
          form={form}
          onSubmit={async (values) => {
            await form.validateFields();
            next();
          }}
          isSubmitting={loading}
          initialValues={initialValues}
        />
      ),
    },
    {
      title: 'Environmental Parameters',
      description: 'Specify environmental impacts',
      validateFields: [
        'electricity_consumption',
        'cooling_consumption',
        'water_consumption',
        'transport_consumption',
        'equipment_mass',
        'allocation_method'
      ],
      component: (
        <EnvironmentalInputForm 
          form={form}
          onSubmit={async (values: EnvironmentalParameters) => {
            await form.validateFields();
            handleSubmit(form.getFieldsValue() as ProcessAnalysis);
          }}
          isSubmitting={loading}
          initialValues={initialValues}
        />
      ),
    },
  ];

  const validateProcessTypeRequirements = (values: ProcessAnalysis) => {
    const errors: string[] = [];
    const { process_type, electricity_consumption, cooling_consumption } = values;

    switch (process_type) {
      case ProcessType.RF:
        if (!electricity_consumption) {
          errors.push('RF process requires electricity consumption');
        }
        break;
      case ProcessType.IR:
        if (!cooling_consumption) {
          errors.push('IR process requires cooling consumption');
        }
        break;
    }

    return errors;
  };

  const handleSubmit = async (values: ProcessAnalysis) => {
    try {
      setLoading(true);

      // Merge with default values
      const processData = {
        ...DEFAULT_PROCESS_ANALYSIS,
        ...values,
      };

      // Validate process requirements
      const errors = validateProcessTypeRequirements(processData);
      if (errors.length > 0) {
        throw new Error(errors.join(', '));
      }

      // Validate mass balance
      if (processData.output_mass > processData.input_mass) {
        throw new Error('Output mass cannot exceed input mass');
      }

      // Validate moisture content
      if (processData.final_moisture_content > processData.initial_moisture_content) {
        throw new Error('Final moisture content cannot exceed initial moisture content');
      }

      // Validate particle size distribution
      if (processData.d50_particle_size <= processData.d10_particle_size ||
          processData.d90_particle_size <= processData.d50_particle_size) {
        throw new Error('Invalid particle size distribution (D10 < D50 < D90)');
      }

      // Submit to API
      const response = await axios.post(
        PROCESS_ENDPOINTS.CREATE,
        processData,
        API_CONFIG
      );

      toast({
        title: "Success",
        description: "Process analysis started successfully",
      });
      onSuccess?.(response.data);
      onSubmit?.(processData);
    } catch (error: any) {
      toast({
        title: "Error",
        description: error.response?.data?.message || error.message || 'Failed to start process analysis',
        variant: "destructive",
      });
    } finally {
      setLoading(false);
    }
  };

  const next = async () => {
    try {
      await form.validateFields(steps[currentStep - 1].validateFields);
      setCurrentStep(currentStep + 1);
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

        <Form
          form={form}
          layout="vertical"
          initialValues={{ ...DEFAULT_PROCESS_ANALYSIS, ...initialValues }}
          onFinish={handleSubmit}
          className="process-form mt-8"
        >
          <div className="steps-content mb-8">
            {steps[currentStep - 1].component}
          </div>

          <div className="flex justify-between mt-8">
            {currentStep > 1 && (
              <Button
                variant="outline"
                onClick={prev}
                disabled={loading || externalLoading}
              >
                Previous
              </Button>
            )}
            {currentStep < steps.length && (
              <Button
                onClick={next}
                disabled={loading || externalLoading}
              >
                Next
              </Button>
            )}
            {currentStep === steps.length && (
              <Button
                type="submit"
                disabled={loading || externalLoading}
              >
                {loading || externalLoading ? "Starting Analysis..." : "Start Analysis"}
              </Button>
            )}
          </div>
        </Form>
      </CardContent>
    </Card>
  );
};

export default ProcessInputForm;
