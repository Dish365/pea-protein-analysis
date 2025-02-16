import { useState } from 'react';
import { useSubmitAnalysis } from './useAnalysis';
import { toast } from '@/hooks/useToast';
import {
  ProcessTypeEnum,
  ProcessStatus,
  ProcessAnalysis,
  TechnicalValidationData,
  EconomicValidationData,
  EnvironmentalValidationData,
  ProcessValidationData,
  technicalValidationSchema,
  economicValidationSchema,
  environmentalValidationSchema,
  processValidationSchema,
  validateProcessData,
  ProcessType
} from '@/types/process';
import { DEFAULT_TECHNICAL_VALUES, DEFAULT_ECONOMIC_VALUES, DEFAULT_ENVIRONMENTAL_VALUES } from '@/components/forms';

export type AnalysisStep = 'technical' | 'economic' | 'environmental' | 'preview';

interface AnalysisState {
  step: AnalysisStep;
  data: {
    technical?: Partial<TechnicalValidationData> & { process_type: ProcessType };
    economic?: EconomicValidationData;
    environmental?: EnvironmentalValidationData;
  };
  isSubmitting: boolean;
  errors: string[];
}

export function useAnalysisFlow() {
  const [state, setState] = useState<AnalysisState>({
    step: 'technical',
    data: {
      technical: { ...DEFAULT_TECHNICAL_VALUES },
      economic: { ...DEFAULT_ECONOMIC_VALUES },
      environmental: { ...DEFAULT_ENVIRONMENTAL_VALUES }
    },
    isSubmitting: false,
    errors: []
  });

  const { mutateAsync: submitAnalysis } = useSubmitAnalysis();

  const validateStep = async (step: AnalysisStep, data: any): Promise<string[]> => {
    const errors: string[] = [];
    
    try {
      switch (step) {
        case 'technical':
          await technicalValidationSchema.parseAsync(data);
          break;
        case 'economic':
          await economicValidationSchema.parseAsync(data);
          break;
        case 'environmental':
          await environmentalValidationSchema.parseAsync(data);
          break;
        case 'preview':
          // Validate complete process data
          await processValidationSchema.parseAsync(data);
          break;
      }
    } catch (error: any) {
      if (error.errors) {
        errors.push(...error.errors.map((e: any) => e.message));
      }
    }
    
    return errors;
  };

  const goToStep = (step: AnalysisStep) => {
    setState(prev => ({ ...prev, step, errors: [] }));
  };

  const handleTechnicalSubmit = async (technicalData: TechnicalValidationData) => {
    const errors = await validateStep('technical', technicalData);
    if (errors.length > 0) {
      setState(prev => ({ ...prev, errors }));
      return;
    }

    setState(prev => ({
      ...prev,
      step: 'economic',
      data: { ...prev.data, technical: technicalData },
      errors: []
    }));
  };

  const handleEconomicSubmit = async (economicData: EconomicValidationData) => {
    const errors = await validateStep('economic', economicData);
    if (errors.length > 0) {
      setState(prev => ({ ...prev, errors }));
      return;
    }

    setState(prev => ({
      ...prev,
      step: 'environmental',
      data: { ...prev.data, economic: economicData },
      errors: []
    }));
  };

  const handleEnvironmentalSubmit = async (environmentalData: EnvironmentalValidationData) => {
    const errors = await validateStep('environmental', environmentalData);
    if (errors.length > 0) {
      setState(prev => ({ ...prev, errors }));
      return;
    }

    setState(prev => ({
      ...prev,
      step: 'preview',
      data: { ...prev.data, environmental: environmentalData },
      errors: []
    }));
  };

  const handleSubmitAnalysis = async () => {
    // Validate complete process data before submission
    const processData = state.data as ProcessValidationData;
    const processErrors = validateProcessData(processData);
    if (processErrors.length > 0) {
      setState(prev => ({ ...prev, errors: processErrors }));
      return;
    }

    // Ensure all required data is present
    if (!state.data.technical || !state.data.economic || !state.data.environmental) {
      setState(prev => ({
        ...prev,
        errors: ["Missing required data. Please complete all steps."]
      }));
      return;
    }

    try {
      setState(prev => ({ ...prev, isSubmitting: true }));
      
      // Prepare submission data
      const { process_type, ...technicalData } = state.data.technical;
      const submissionData = {
        id: '', // Will be assigned by backend
        process_type,
        timestamp: new Date().toISOString(),
        status: ProcessStatus.PENDING,
        progress: 0,
        
        // Technical parameters
        ...technicalData,
        
        // Economic parameters
        ...state.data.economic,
        
        // Environmental parameters
        ...state.data.environmental,
        
        // Default values for backend-populated fields
        labor_config: {
          hourly_wage: state.data.economic.labor_cost,
          hours_per_week: state.data.economic.operating_hours / 52,
          weeks_per_year: 52,
          num_workers: 1
        },
        cash_flows: [],
        energy_consumption: {},
        production_data: {},
        product_values: {},
        hybrid_weights: state.data.environmental.hybrid_weights || {},
        sensitivity_range: 0.1,
        steps: 10,
        technical_results: undefined,
        economic_results: undefined,
        environmental_results: undefined,
        efficiency_results: undefined
      } as ProcessAnalysis;

      const result = await submitAnalysis(submissionData);
      toast({
        title: "Success",
        description: "Analysis submitted successfully",
      });
      return result.id;
    } catch (error: any) {
      setState(prev => ({
        ...prev,
        errors: [error.message || "Failed to submit analysis"]
      }));
      toast({
        title: "Error",
        description: error.message || "Failed to submit analysis",
        variant: "destructive",
      });
    } finally {
      setState(prev => ({ ...prev, isSubmitting: false }));
    }
  };

  return {
    step: state.step,
    data: state.data,
    errors: state.errors,
    isSubmitting: state.isSubmitting,
    goToStep,
    handleTechnicalSubmit,
    handleEconomicSubmit,
    handleEnvironmentalSubmit,
    handleSubmitAnalysis
  };
} 