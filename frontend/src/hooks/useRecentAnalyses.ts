import { useQuery } from '@tanstack/react-query';
import { ProcessType, ProcessStatus } from '@/types/process';

export interface Analysis {
  id: string;
  type: ProcessType;
  status: ProcessStatus;
  startedAt: string;
  completedAt?: string;
}

async function fetchRecentAnalyses(): Promise<Analysis[]> {
  const response = await fetch('/api/analyses/recent');
  if (!response.ok) {
    throw new Error('Failed to fetch recent analyses');
  }
  return response.json();
}

export function useRecentAnalyses() {
  return useQuery({
    queryKey: ['recentAnalyses'],
    queryFn: fetchRecentAnalyses,
    refetchInterval: 30000, // Refetch every 30 seconds
    staleTime: 10000, // Consider data stale after 10 seconds
  });
} 