import { AnalysisResultsClient } from './AnalysisResultsClient';
import api from '@/lib/axios';
import { API_ENDPOINTS } from '@/config/api';
import { ApiResponse } from '@/types/api';
import { ProcessAnalysis } from '@/types/process';

interface AnalysisResultsPageProps {
  params: {
    id: string;
  };
}

export default async function AnalysisResultsPage({ params }: AnalysisResultsPageProps) {
  let initialData = null;

  try {
    const response = await api.get<ApiResponse<ProcessAnalysis>>(
      API_ENDPOINTS.process.results(params.id)
    );
    initialData = response.data.data || null;
  } catch (error) {
    console.error('Failed to fetch initial analysis data:', error);
  }

  return <AnalysisResultsClient analysisId={params.id} initialData={initialData} />;
} 