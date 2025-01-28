import React, { useState } from 'react';
import { Form, Steps, Button, message, Card } from 'antd';
import { ProcessAnalysis } from '@/types/process';
import { DEFAULT_PROCESS_ANALYSIS } from '@/config/constants';
import TechnicalInputForm from './TechnicalInputForm';
import EconomicInputForm from './EconomicInputForm';
import EnvironmentalInputForm from './EnvironmentalInputForm';
import { PROCESS_ENDPOINTS, API_CONFIG } from '@/config/endpoints';
import axios from 'axios';

const { Step } = Steps;

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
  const [currentStep, setCurrentStep] = useState(0);
  const [loading, setLoading] = useState(false);
  const [formData, setFormData] = useState(initialValues);

  const handleSubmit = async (values: Partial<ProcessAnalysis>) => {
    try {
      setLoading(true);
      
      // Combine all form data
      const processData = {
        ...DEFAULT_PROCESS_ANALYSIS,
        ...formData,
        ...values,
      };

      // Validate process requirements
      const errors = validateProcessTypeRequirements(processData as ProcessAnalysis);
      if (errors.length > 0) {
        throw new Error(errors.join(', '));
      }

      // Submit to API
      const response = await axios.post(
        PROCESS_ENDPOINTS.CREATE,
        processData,
        API_CONFIG
      );

      message.success('Process analysis started successfully');
      onSuccess?.(response.data);
      onSubmit?.(processData as ProcessAnalysis);
    } catch (error: any) {
      message.error(error.response?.data?.message || error.message || 'Failed to start process analysis');
    } finally {
      setLoading(false);
    }
  };

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
          onSubmit={async (values) => {
            setFormData(prev => ({ ...prev, ...values }));
            next();
          }}
          initialValues={formData}
          isSubmitting={loading}
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
        'revenue_per_year',
      ],
      component: (
        <EconomicInputForm
          onSubmit={async (values) => {
            setFormData(prev => ({ ...prev, ...values }));
            next();
          }}
          initialValues={formData}
          isSubmitting={loading}
        />
      ),
    },
    {
      title: 'Environmental Parameters',
      description: 'Specify environmental impacts',
      validateFields: [
        'electricity_consumption',
        'thermal_energy',
        'cooling_consumption',
        'water_consumption',
        'wastewater_generation',
        'solid_waste',
        'recyclable_waste',
        'transport_distance',
        'transport_load',
        'equipment_mass',
      ],
      component: (
        <EnvironmentalInputForm
          onSubmit={handleSubmit}
          initialValues={formData}
          isSubmitting={loading}
        />
      ),
    },
  ];

  const validateProcessTypeRequirements = (values: ProcessAnalysis) => {
    const errors: string[] = [];
    const { process_type, electricity_consumption, cooling_consumption } = values;

    switch (process_type) {
      case 'rf':
        if (!electricity_consumption) {
          errors.push('RF process requires electricity consumption');
        }
        break;
      case 'ir':
        if (!cooling_consumption) {
          errors.push('IR process requires cooling consumption');
        }
        break;
    }

    return errors;
  };

  const next = () => {
    setCurrentStep(currentStep + 1);
  };

  const prev = () => {
    setCurrentStep(currentStep - 1);
  };

  return (
    <Card className="max-w-4xl mx-auto">
      <Steps current={currentStep} className="mb-8">
        {steps.map(({ title, description }) => (
          <Step key={title} title={title} description={description} />
        ))}
      </Steps>

      <div className="steps-content mb-8">
        {steps[currentStep].component}
      </div>

      <div className="flex justify-between mt-8">
        {currentStep > 0 && (
          <Button 
            onClick={prev}
            disabled={loading || externalLoading}
          >
            Previous
          </Button>
        )}
        <div className="flex-1" />
        {currentStep < steps.length - 1 && (
          <Button 
            type="primary"
            onClick={next}
            disabled={loading || externalLoading}
          >
            Next
          </Button>
        )}
      </div>
    </Card>
  );
};

export default ProcessInputForm;
