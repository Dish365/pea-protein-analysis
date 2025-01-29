import { useQuery } from '@tanstack/react-query';
import type { Query } from '@tanstack/react-query';
import axios from 'axios';
import { PROCESS_ENDPOINTS } from '@/config/endpoints';
import { ProcessType, ProcessStatus } from '@/types/process';

export interface Analysis {
  id: string;
  type: ProcessType;
  status: ProcessStatus;
  startedAt: string;
  completedAt?: string;
  results?: {
    technical?: any;
    economic?: any;
    environmental?: any;
  };
  error?: string;
}

export interface ProcessListResponse {
  data: Analysis[];
  total: number;
  page: number;
  pageSize: number;
}

export const useRecentAnalyses = (limit: number = 5) => {
  return useQuery<ProcessListResponse>({
    queryKey: ['recentAnalyses', limit],
    queryFn: async () => {
      const { data } = await axios.get<ProcessListResponse>(
        `${PROCESS_ENDPOINTS.LIST}?limit=${limit}`
      );
      return data;
    },
    staleTime: 30000,
    refetchInterval: (query) => {
      const hasInProgress = query.state.data?.data.some(
        (analysis) => analysis.status === ProcessStatus.PROCESSING 
      );
      return hasInProgress ? 5000 : false;
    },
  });
};
