import { useQuery, useMutation } from '@tanstack/react-query';
import axios from 'axios';
import { PROCESS_ENDPOINTS, API_CONFIG } from '@/config/endpoints';
import { ProcessAnalysis } from '@/types/process';
import { AnalysisResult, ProcessCreateResponse } from '@/types/api';

export function useAnalysisResults(analysisId: number | null) {
  return useQuery({
    queryKey: ['analysis', analysisId],
    queryFn: async () => {
      if (!analysisId) return null;
      const response = await axios.get(
        PROCESS_ENDPOINTS.RESULTS(analysisId),
        API_CONFIG
      );
      return response.data as AnalysisResult;
    },
    enabled: !!analysisId,
    refetchInterval: (query) => {
      const data = query.state.data as AnalysisResult | null;
      const status = data?.process_status;
      if (!data || status === 'completed' || status === 'failed') {
        return false;
      }
      return 1000;
    },
  });
}

export function useSubmitAnalysis() {
  return useMutation({
    mutationFn: async (data: Partial<ProcessAnalysis>) => {
      const response = await axios.post(
        PROCESS_ENDPOINTS.CREATE,
        data,
        API_CONFIG
      );
      return response.data as ProcessCreateResponse;
    },
  });
} 