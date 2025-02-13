import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import api from "@/lib/axios";
import { API_ENDPOINTS } from "@/config/api";
import { ProcessAnalysis, ProcessStatus } from "@/types/process";
import { ProcessCreateResponse, ProcessDetailResponse, ApiResponse } from "@/types/api";

const POLLING_INTERVAL = 5000; // 5 seconds
const MAX_RETRIES = 3;

/**
 * Hook for submitting a new process analysis
 */
export function useSubmitAnalysis() {
  const queryClient = useQueryClient();

  return useMutation<ProcessDetailResponse, Error, ProcessAnalysis>({
    mutationFn: async (data: ProcessAnalysis) => {
      try {
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
      } catch (error: any) {
        throw new Error(error.response?.data?.error || 'Failed to submit analysis');
      }
    },
    onSuccess: (data) => {
      // Update cache with new results
      queryClient.setQueryData(['analysis', data.id], data);
    },
    retry: MAX_RETRIES,
    retryDelay: (attemptIndex) => Math.min(1000 * 2 ** attemptIndex, 30000)
  });
}

/**
 * Hook for fetching and polling analysis results
 */
export function useAnalysisResults(analysisId: string | null) {
  const queryClient = useQueryClient();

  return useQuery<ProcessDetailResponse>({
    queryKey: ["analysis", analysisId],
    queryFn: async () => {
      if (!analysisId) {
        throw new Error("No analysis ID provided");
      }

      try {
        const response = await api.get<ApiResponse<ProcessDetailResponse>>(
          API_ENDPOINTS.process.results(analysisId)
        );

        if (!response.data.data) {
          throw new Error("Failed to fetch analysis results");
        }

        return response.data.data;
      } catch (error: any) {
        // Handle specific error cases
        if (error.response?.status === 404) {
          throw new Error("Analysis not found");
        }
        throw new Error(error.response?.data?.error || "Failed to fetch analysis results");
      }
    },
    enabled: !!analysisId,
    refetchInterval: (query) => {
      const data = query.state.data;
      // Stop polling if analysis is complete or failed
      if (data?.status === ProcessStatus.COMPLETED || 
          data?.status === ProcessStatus.FAILED) {
        return false;
      }
      // Continue polling for in-progress analyses
      return POLLING_INTERVAL;
    },
    // Retry configuration
    retry: MAX_RETRIES,
    retryDelay: (attemptIndex) => Math.min(1000 * 2 ** attemptIndex, 30000),
    // Stale time configuration
    staleTime: 30000, // Consider data stale after 30 seconds
    gcTime: 3600000 // Keep in cache for 1 hour
  });
}

/**
 * Hook for fetching analysis status
 */
export function useAnalysisStatus(analysisId: string | null) {
  return useQuery<ProcessStatus>({
    queryKey: ["analysis-status", analysisId],
    queryFn: async () => {
      if (!analysisId) {
        throw new Error("No analysis ID provided");
      }

      const response = await api.get<ApiResponse<{ status: ProcessStatus }>>(
        API_ENDPOINTS.process.status(analysisId)
      );

      if (!response.data.data?.status) {
        throw new Error("Failed to fetch analysis status");
      }

      return response.data.data.status;
    },
    enabled: !!analysisId,
    // More frequent polling for status updates
    refetchInterval: (query) => {
      const status = query.state.data;
      return status === ProcessStatus.COMPLETED || 
             status === ProcessStatus.FAILED 
        ? false 
        : 2000; // Poll every 2 seconds for status
    },
    staleTime: 0, // Always fetch fresh status
    gcTime: 3600000 // Keep in cache for 1 hour
  });
}
