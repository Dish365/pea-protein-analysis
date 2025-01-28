import { useQuery } from '@tanstack/react-query';
import axios from 'axios';
import { PROCESS_ENDPOINTS, API_CONFIG } from '@/config/endpoints';
import { ProcessListResponse } from '@/types/api';

export function useRecentAnalyses() {
  return useQuery({
    queryKey: ['recentAnalyses'],
    queryFn: async () => {
      const response = await axios.get(
        PROCESS_ENDPOINTS.LIST,
        API_CONFIG
      );
      return response.data as ProcessListResponse;
    },
    refetchInterval: 30000, // Refetch every 30 seconds
    staleTime: 10000, // Consider data stale after 10 seconds
  });
} 