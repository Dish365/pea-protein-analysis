import { useState } from 'react';
import { useMutation } from '@tanstack/react-query';
import api from '@/lib/axios';
import { API_ENDPOINTS } from '@/config/api';
import { useToast } from '@/hooks/useToast';
import { TechnicalParameters } from '@/types/technical';
import { EconomicParameters } from '@/types/economic';
import { EnvironmentalParameters } from '@/types/environmental';

interface AnalysisState {
  id?: string;
  step: 'technical' | 'economic' | 'environmental' | 'complete';
  data: {
    technical?: TechnicalParameters;
    economic?: EconomicParameters;
    environmental?: EnvironmentalParameters;
  };
}

export function useAnalysisFlow() {
  const [state, setState] = useState<AnalysisState>({
    step: 'technical',
    data: {}
  });
  const { toast } = useToast();

  // Create analysis
  const createAnalysis = useMutation({
    mutationFn: async () => {
      const response = await api.post(API_ENDPOINTS.analysis.create);
      return response.data;
    },
    onSuccess: (data) => {
      setState(prev => ({
        ...prev,
        id: data.id
      }));
    },
    onError: (error: any) => {
      toast({
        title: "Error",
        description: error.response?.data?.error || "Failed to create analysis",
        variant: "destructive"
      });
    }
  });

  // Update step
  const updateStep = useMutation({
    mutationFn: async (stepData: {
      type: 'technical' | 'economic' | 'environmental';
      parameters: any;
    }) => {
      if (!state.id) throw new Error("No analysis ID");
      const response = await api.put(
        API_ENDPOINTS.analysis.update(state.id),
        stepData
      );
      return response.data;
    },
    onSuccess: (_, variables) => {
      // Update local state
      setState(prev => ({
        ...prev,
        data: {
          ...prev.data,
          [variables.type]: variables.parameters
        },
        step: getNextStep(variables.type)
      }));

      toast({
        title: "Success",
        description: `${variables.type.charAt(0).toUpperCase() + variables.type.slice(1)} parameters saved successfully`,
      });
    },
    onError: (error: any) => {
      toast({
        title: "Error",
        description: error.response?.data?.error || "Failed to update analysis",
        variant: "destructive"
      });
    }
  });

  // Submit analysis
  const submitAnalysis = useMutation({
    mutationFn: async () => {
      if (!state.id) throw new Error("No analysis ID");
      const response = await api.post(
        API_ENDPOINTS.analysis.submit(state.id)
      );
      return response.data;
    },
    onSuccess: (data) => {
      setState(prev => ({
        ...prev,
        step: 'complete'
      }));
      toast({
        title: "Success",
        description: "Analysis submitted successfully",
      });
    },
    onError: (error: any) => {
      toast({
        title: "Error",
        description: error.response?.data?.error || "Failed to submit analysis",
        variant: "destructive"
      });
    }
  });

  const getNextStep = (currentStep: string): AnalysisState['step'] => {
    switch (currentStep) {
      case 'technical':
        return 'economic';
      case 'economic':
        return 'environmental';
      case 'environmental':
        return 'complete';
      default:
        return 'complete';
    }
  };

  const handleTechnicalSubmit = async (data: TechnicalParameters) => {
    if (!state.id) {
      await createAnalysis.mutateAsync();
    }
    await updateStep.mutateAsync({ type: 'technical', parameters: data });
  };

  const handleEconomicSubmit = async (data: EconomicParameters) => {
    await updateStep.mutateAsync({ type: 'economic', parameters: data });
  };

  const handleEnvironmentalSubmit = async (data: EnvironmentalParameters) => {
    await updateStep.mutateAsync({ type: 'environmental', parameters: data });
    await submitAnalysis.mutateAsync();
  };

  return {
    state,
    isLoading: createAnalysis.isLoading || updateStep.isLoading || submitAnalysis.isLoading,
    handleTechnicalSubmit,
    handleEconomicSubmit,
    handleEnvironmentalSubmit
  };
} 