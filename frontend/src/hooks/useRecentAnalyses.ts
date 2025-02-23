import { useQuery } from "@tanstack/react-query";
import api from "@/lib/axios";
import { API_ENDPOINTS } from "@/config/api";
import { ProcessType, ProcessStatus } from "@/types/process";
import { ApiResponse, ProcessListResponse } from "@/types/api";

export interface RecentAnalysis {
  id: string;
  type: ProcessType;
  status: ProcessStatus;
  created_at: string;
  updated_at: string;
  results?: {
    technical?: Record<string, unknown>;
    economic?: Record<string, unknown>;
    environmental?: Record<string, unknown>;
  };
  progress: number;
}

/**
 * Hook for fetching recent analyses with pagination
 */
export function useRecentAnalyses(page = 1, pageSize = 10) {
  return useQuery<ProcessListResponse>({
    queryKey: ["recentAnalyses", page, pageSize],
    queryFn: async () => {
      const response = await api.get<ApiResponse<ProcessListResponse>>(
        API_ENDPOINTS.analysis.list,
        {
          params: {
            page,
            page_size: pageSize,
          },
        }
      );

      if (!response.data.data) {
        throw new Error("Failed to fetch recent analyses");
      }

      return response.data.data;
    },
    // Keep data fresh but don't refetch too often
    staleTime: 30000, // 30 seconds
    refetchInterval: 60000, // 1 minute
  });
}
