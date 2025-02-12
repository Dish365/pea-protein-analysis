"use client";

import React from 'react';
import { useQuery } from '@tanstack/react-query';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { LoadingSpinner } from "@/components/ui/loading-spinner";
import { TechnicalAnalysisView } from '@/features/analysis/technical/components/TechnicalAnalysisView';
import { EconomicAnalysisView } from '@/features/analysis/economic/components/EconomicAnalysisView';
import { EnvironmentalAnalysisView } from '@/features/analysis/environmental/components/EnvironmentalAnalysisView';
import api from '@/lib/axios';
import { API_ENDPOINTS } from '@/config/api';
import { ProcessStatus } from '@/types/process';
import { AnalysisResult } from '@/types/api';

interface AnalysisResultsClientProps {
  analysisId: string;
  initialData: AnalysisResult | null;
}

export function AnalysisResultsClient({ analysisId, initialData }: AnalysisResultsClientProps) {
  // Fetch analysis results
  const { data: analysis, isLoading, error } = useQuery<AnalysisResult>({
    queryKey: ['analysis', analysisId],
    queryFn: async () => {
      if (!analysisId) throw new Error('No analysis ID provided');
      try {
        const response = await api.get<AnalysisResult>(API_ENDPOINTS.process.results(analysisId));
        return response.data;
      } catch (err) {
        console.error('Error fetching analysis:', err);
        throw err;
      }
    },
    initialData: initialData || undefined,
    refetchInterval: (queryInfo) => {
      const data = queryInfo.state.data;
      if (data?.status === ProcessStatus.PROCESSING || 
          data?.status === ProcessStatus.PENDING) {
        return 5000;
      }
      return false;
    },
    // Disable retries on error
    retry: false,
    // Ensure stale data is not used
    staleTime: 0
  });

  if (!analysisId) {
    return (
      <Alert>
        <AlertDescription>No analysis ID provided</AlertDescription>
      </Alert>
    );
  }

  if (isLoading) {
    return <LoadingSpinner />;
  }

  if (error) {
    return (
      <Alert>
        <AlertDescription>Error loading analysis results</AlertDescription>
      </Alert>
    );
  }

  if (!analysis) {
    return (
      <Alert>
        <AlertDescription>No analysis data found</AlertDescription>
      </Alert>
    );
  }

  const isProcessing = analysis.status === ProcessStatus.PROCESSING;
  const hasFailed = analysis.status === ProcessStatus.FAILED;

  return (
    <div className="space-y-6">
      {/* Technical Analysis Results */}
      <Card>
        <CardHeader>
          <CardTitle>Technical Analysis Results</CardTitle>
        </CardHeader>
        <CardContent>
          <TechnicalAnalysisView
            data={analysis.results?.technical}
            isLoading={isProcessing}
            error={hasFailed ? "Analysis failed" : undefined}
          />
        </CardContent>
      </Card>

      {/* Economic Analysis Results */}
      <Card>
        <CardHeader>
          <CardTitle>Economic Analysis Results</CardTitle>
        </CardHeader>
        <CardContent>
          <EconomicAnalysisView
            data={analysis.results?.economic?.results}
            isLoading={isProcessing}
            error={hasFailed ? "Analysis failed" : undefined}
          />
        </CardContent>
      </Card>

      {/* Environmental Analysis Results */}
      <Card>
        <CardHeader>
          <CardTitle>Environmental Analysis Results</CardTitle>
        </CardHeader>
        <CardContent>
          <EnvironmentalAnalysisView
            data={analysis.results?.environmental?.results}
            isLoading={isProcessing}
            error={hasFailed ? "Analysis failed" : undefined}
          />
        </CardContent>
      </Card>
    </div>
  );
} 