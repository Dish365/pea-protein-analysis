import { useQuery } from "@tanstack/react-query";
import axios from "axios";
import { PROCESS_ENDPOINTS, API_CONFIG } from "@/config/endpoints";
import { ProcessListResponse } from "@/types/api";
import { ProcessType, ProcessStatus } from "@/types/process";

export interface Analysis {
  id: string;
  type: ProcessType;
  status: ProcessStatus;
  startedAt: string;
  completedAt?: string;
}

export function useRecentAnalyses() {
  const { data, isLoading, isError, error } = useQuery<Analysis[]>({
    queryKey: ["recentAnalyses"],
    queryFn: async () => {
      const response = await fetch("/api/analyses");
      return response.json();
    },
  });

  return { data, isLoading, isError, error };
}
