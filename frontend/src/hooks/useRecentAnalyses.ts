import { useQuery } from "@tanstack/react-query";
import api from "@/lib/axios";
import { API_ENDPOINTS } from "@/config/api";
import { ProcessType, ProcessStatus } from "@/types/process";

export interface Analysis {
  id: string;
  type: "technical" | "economic" | "environmental";
  status: ProcessStatus;
  date: string;
  results?: {
    technical?: any;
    economic?: any;
    environmental?: any;
  };
  progress: number;
}

export function useRecentAnalyses() {
  return useQuery({
    queryKey: ["recentAnalyses"],
    queryFn: async () => {
      const response = await api.get(API_ENDPOINTS.process.submit);
      return response.data;
    },
  });
}
