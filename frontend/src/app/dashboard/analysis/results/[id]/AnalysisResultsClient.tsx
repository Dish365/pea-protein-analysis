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
import { ApiResponse } from '@/types/api';
import { ProcessAnalysis } from '@/types/process';
import { TechnicalResults } from '@/types/technical';
import { EconomicResults } from '@/types/economic';
import { EnvironmentalResults } from '@/types/environmental';

interface AnalysisResultsClientProps {
  analysisId: string;
  initialData: ProcessAnalysis | null;
}

export function AnalysisResultsClient({ analysisId, initialData }: AnalysisResultsClientProps) {
  const { data: analysis, isLoading, error } = useQuery({
    queryKey: ['analysis', analysisId],
    queryFn: async () => {
      const response = await api.get<ApiResponse<ProcessAnalysis>>(
        API_ENDPOINTS.process.results(analysisId)
      );
      if (!response.data.data) {
        throw new Error('No analysis data found');
      }
      return response.data.data;
    },
    initialData: initialData || undefined,
    refetchInterval: (query) => {
      const data = query.state.data;
      // Stop polling if analysis is complete or failed
      if (!data || 
          data.status === ProcessStatus.COMPLETED || 
          data.status === ProcessStatus.FAILED) {
        return false;
      }
      // Continue polling for in-progress analyses
      return 5000; // Poll every 5 seconds
    }
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

  // Cast results to their proper types
  const technicalResults = analysis.technical_results as TechnicalResults | undefined;
  const economicResults = analysis.economic_results as EconomicResults | undefined;
  const environmentalResults = analysis.environmental_results as EnvironmentalResults | undefined;

  return (
    <div className="space-y-6 p-6">
      {/* Status Banner */}
      {isProcessing && (
        <Alert>
          <LoadingSpinner className="mr-2 h-4 w-4" />
          <AlertDescription>Analysis in progress...</AlertDescription>
        </Alert>
      )}
      
      {hasFailed && (
        <Alert variant="destructive">
          <AlertDescription>Analysis failed to complete</AlertDescription>
        </Alert>
      )}

      {/* Technical Analysis Results */}
      <Card>
        <CardHeader>
          <CardTitle>Technical Analysis Results</CardTitle>
        </CardHeader>
        <CardContent>
          <TechnicalAnalysisView
            data={technicalResults}
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
            data={economicResults}
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
            data={environmentalResults}
            isLoading={isProcessing}
            error={hasFailed ? "Analysis failed" : undefined}
          />
        </CardContent>
      </Card>

      {/* Efficiency Results */}
      {analysis.efficiency_results && (
        <Card>
          <CardHeader>
            <CardTitle>Overall Process Efficiency</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid gap-4 md:grid-cols-2">
              <div>
                <h3 className="text-lg font-medium">Efficiency Metrics</h3>
                <dl className="mt-2 space-y-2">
                  <div>
                    <dt className="text-sm text-muted-foreground">Eco-Efficiency Index</dt>
                    <dd className="text-2xl font-bold">
                      {analysis.efficiency_results.efficiency_metrics?.eco_efficiency_index.toFixed(2)}
                    </dd>
                  </div>
                </dl>
              </div>
              <div>
                <h3 className="text-lg font-medium">Performance Indicators</h3>
                <dl className="mt-2 space-y-2">
                  <div>
                    <dt className="text-sm text-muted-foreground">Relative Performance</dt>
                    <dd className="text-2xl font-bold">
                      {analysis.efficiency_results.performance_indicators?.relative_performance.toFixed(2)}
                    </dd>
                  </div>
                </dl>
              </div>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
} 