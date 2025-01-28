import { useQuery, useMutation } from '@tanstack/react-query';
import axios from 'axios';
import { ENDPOINTS } from '@/config/endpoints';
import { ProcessAnalysis } from '@/types/process';

export function useAnalysisResults(analysisId: string | null) {
  return useQuery({
    queryKey: ['analysis', analysisId],
    queryFn: async () => {
      if (!analysisId) return null;
      const response = await axios.get(
        `${ENDPOINTS.PROCESS.RESULTS(parseInt(analysisId))}`
      );
      return response.data.results as ProcessAnalysis;
    },
    enabled: !!analysisId,
    refetchInterval: (data) => {
      if (!data || data.status === 'completed' || data.status === 'failed') {
        return false;
      }
      return 1000; // Poll every second while in progress
    },
  });
}

export function useSubmitAnalysis() {
  return useMutation({
    mutationFn: async (data: Partial<ProcessAnalysis>) => {
      const response = await axios.post(
        ENDPOINTS.PROCESS.CREATE,
        data
      );
      return response.data;
    },
  });
} 