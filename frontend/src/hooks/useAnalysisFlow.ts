import { useState } from 'react';
import { useSubmitAnalysis } from './useAnalysis';
import { toast } from '@/hooks/useToast';
import {
  ProcessTypeEnum,
  ProcessStatus,
  ProcessAnalysis,
  TechnicalData,
  EconomicData,
  EnvironmentalData,
  ProcessData,
  validateProcessData,
  technicalSchema,
  economicSchema,
  environmentalSchema
} from '@/types/process';

export type AnalysisStep = 'technical' | 'economic' | 'environmental';

interface AnalysisState {
  step: AnalysisStep;
  data: Partial<ProcessData>;
  isSubmitting: boolean;
  errors: string[];
}

export function useAnalysisFlow() {
  const [state, setState] = useState<AnalysisState>({
    step: 'technical',
    data: {
      technical: {
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
        d90_particle_size: 0
      }
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
          await technicalSchema.parseAsync(data);
          break;
        case 'economic':
          await economicSchema.parseAsync(data);
          break;
        case 'environmental':
          await environmentalSchema.parseAsync(data);
          break;
      }
    } catch (error: any) {
      if (error.errors) {
        errors.push(...error.errors.map((e: any) => e.message));
      }
    }
    
    return errors;
  };

  const handleTechnicalSubmit = async (technicalData: TechnicalData) => {
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

  const handleEconomicSubmit = async (economicData: EconomicData) => {
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

  const handleEnvironmentalSubmit = async (environmentalData: EnvironmentalData) => {
    const errors = await validateStep('environmental', environmentalData);
    if (errors.length > 0) {
      setState(prev => ({ ...prev, errors }));
      return;
    }

    setState(prev => ({
      ...prev,
      data: { ...prev.data, environmental: environmentalData },
      errors: []
    }));

    // Prepare submission data
    const { process_type, ...technicalData } = state.data.technical!;
    const submissionData: ProcessAnalysis = {
      id: '', // Will be assigned by backend
      process_type,
      timestamp: new Date().toISOString(),
      status: ProcessStatus.PENDING,
      progress: 0,
      
      // Technical parameters
      ...technicalData,
      
      // Economic parameters
      ...state.data.economic!,
      
      // Environmental parameters
      ...environmentalData,
      
      // Default values for backend-populated fields
      equipment: [],
      maintenance_cost: 0,
      indirect_factors: [],
      utilities: [],
      raw_materials: [],
      labor_config: {
        hourly_wage: state.data.economic!.labor_cost,
        hours_per_week: state.data.economic!.operating_hours / 52,
        weeks_per_year: 52,
        num_workers: 1
      },
      cash_flows: [],
      energy_consumption: {},
      production_data: {},
      product_values: {},
      hybrid_weights: environmentalData.hybrid_weights || {},
      sensitivity_range: 0.1,
      steps: 10,
      technical_results: undefined,
      economic_results: undefined,
      environmental_results: undefined,
      efficiency_results: undefined
    };

    try {
      setState(prev => ({ ...prev, isSubmitting: true }));
      await submitAnalysis(submissionData);
      toast({
        title: "Success",
        description: "Analysis submitted successfully",
      });
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
    handleTechnicalSubmit,
    handleEconomicSubmit,
    handleEnvironmentalSubmit
  };
} 