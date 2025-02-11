import { useQuery, useMutation } from "@tanstack/react-query";
import api from "@/lib/axios";
import { API_ENDPOINTS } from "@/config/api";
import type { ProcessAnalysis } from "@/types/process";
import { AnalysisResult } from "@/types/api";

export function useSubmitAnalysis() {
  return useMutation({
    mutationFn: async (data: ProcessAnalysis) => {
      // First, submit to Django to create analysis record
      const processResponse = await api.post(API_ENDPOINTS.process.submit, {
        process_type: data.type,
        status: "pending",
        ...data.parameters,
      });

      const analysisId = processResponse.data.id;

      // Then trigger FastAPI analysis pipeline
      const analysisResponse = await api.post(
        `${API_ENDPOINTS.process.analyze}/${analysisId}`,
        data
      );

      return {
        analysisId,
        ...analysisResponse.data,
      };
    },
  });
}

export function useAnalysisResults(analysisId: string | null) {
  return useQuery({
    queryKey: ["analysis", analysisId],
    queryFn: async () => {
      if (!analysisId) throw new Error("No analysis ID");

      // Get results from Django
      const response = await api.get(
        API_ENDPOINTS.process.getResults(analysisId)
      );

      return response.data;
    },
    enabled: !!analysisId,
    // Poll until analysis is complete
    refetchInterval: (data) => (data?.status === "completed" ? false : 5000),
  });
}
