import { useQuery, useMutation } from "@tanstack/react-query";
import api from "@/lib/axios";
import { API_ENDPOINTS } from "@/config/api";
import type { ProcessAnalysis } from "@/types/process";
import { AnalysisResult, ProcessCreateResponse } from "@/types/api";
import axios from "axios";

export function useAnalysisResults(analysisId: string | null) {
  return useQuery({
    queryKey: ["analysis", analysisId],
    queryFn: async () => {
      if (!analysisId) throw new Error("No analysis ID");
      try {
        const response = await api.get(
          API_ENDPOINTS.process.getResults(analysisId)
        );
        return response.data;
      } catch (error) {
        // Handle specific error cases
        if (axios.isAxiosError(error)) {
          if (error.response?.status === 404) {
            throw new Error("Analysis not found");
          }
          if (error.response?.status === 401) {
            throw new Error("Unauthorized");
          }
        }
        throw error;
      }
    },
    enabled: !!analysisId,
    refetchInterval: (data) => (data?.status === "completed" ? false : 5000), // Poll every 5s until complete
  });
}

export function useSubmitAnalysis() {
  return useMutation({
    mutationFn: async (data: ProcessAnalysis) => {
      const response = await api.post(API_ENDPOINTS.process.submit, data);
      return response.data;
    },
  });
}
