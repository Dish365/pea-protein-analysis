import { useQuery, useMutation } from "@tanstack/react-query";
import api from "@/lib/axios";
import { API_ENDPOINTS } from "@/config/api";
import { ProcessAnalysis, ProcessStatus } from "@/types/process";
import { ProcessCreateResponse, ProcessDetailResponse, ApiResponse } from "@/types/api";

/**
 * Hook for submitting a new process analysis
 */
export function useSubmitAnalysis() {
  return useMutation<ProcessDetailResponse, Error, ProcessAnalysis>({
    mutationFn: async (data: ProcessAnalysis) => {
      // Create analysis record in Django backend
      const processResponse = await api.post<ApiResponse<ProcessCreateResponse>>(
        API_ENDPOINTS.process.create,
        data
      );

      if (!processResponse.data.data?.id) {
        throw new Error("Failed to create analysis record");
      }

      const analysisId = processResponse.data.data.id;

      // Get analysis results
      const analysisResponse = await api.get<ApiResponse<ProcessDetailResponse>>(
        API_ENDPOINTS.process.results(analysisId)
      );

      if (!analysisResponse.data.data) {
        throw new Error("Failed to fetch analysis results");
      }

      return analysisResponse.data.data;
    },
  });
}

/**
 * Hook for fetching and polling analysis results
 */
export function useAnalysisResults(analysisId: string | null) {
  return useQuery<ProcessDetailResponse>({
    queryKey: ["analysis", analysisId],
    queryFn: async () => {
      if (!analysisId) {
        throw new Error("No analysis ID provided");
      }

      const response = await api.get<ApiResponse<ProcessDetailResponse>>(
        API_ENDPOINTS.process.results(analysisId)
      );

      if (!response.data.data) {
        throw new Error("Failed to fetch analysis results");
      }

      return response.data.data;
    },
    enabled: !!analysisId,
    refetchInterval: (query) => {
      const data = query.state.data;
      return data?.status === ProcessStatus.COMPLETED || 
             data?.status === ProcessStatus.FAILED 
        ? false 
        : 5000; // Poll every 5 seconds until complete
    },
  });
}
