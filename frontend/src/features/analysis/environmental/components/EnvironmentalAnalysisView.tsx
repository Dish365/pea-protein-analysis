"use client";

import React from 'react';
import { AlertCircle, Loader2 } from 'lucide-react';
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { Card } from '@/components/ui/card';
import { Skeleton } from '@/components/ui/skeleton';
import { EnvironmentalResults } from '@/types/environmental';
import { EmissionsBreakdown } from './EmissionsBreakdown';
import { ImpactMetrics } from './ImpactMetrics';
import { ResourceConsumption } from './ResourceConsumption';
import { SustainabilityScore } from './SustainabilityScore';

interface EnvironmentalAnalysisViewProps {
  data?: EnvironmentalResults;
  isLoading?: boolean;
  error?: string;
}

export function EnvironmentalAnalysisView({
  data,
  isLoading,
  error
}: EnvironmentalAnalysisViewProps) {
  if (isLoading) {
    return (
      <div className="space-y-6">
        <div className="grid gap-6 md:grid-cols-2">
          <Card className="p-6">
            <div className="space-y-4">
              <div className="flex items-center space-x-4">
                <Loader2 className="h-4 w-4 animate-spin" />
                <Skeleton className="h-4 w-[200px]" />
              </div>
              <div className="space-y-2">
                <Skeleton className="h-4 w-[180px]" />
                <Skeleton className="h-4 w-[150px]" />
                <Skeleton className="h-4 w-[160px]" />
              </div>
            </div>
          </Card>
          <Card className="p-6">
            <div className="space-y-4">
              <Skeleton className="h-4 w-[250px]" />
              <div className="grid grid-cols-2 gap-4">
                <Skeleton className="h-20 w-full" />
                <Skeleton className="h-20 w-full" />
                <Skeleton className="h-20 w-full" />
                <Skeleton className="h-20 w-full" />
              </div>
            </div>
          </Card>
        </div>
        <div className="grid gap-6 md:grid-cols-2">
          <Card className="p-6">
            <div className="space-y-4">
              <Skeleton className="h-4 w-[220px]" />
              <div className="h-[200px] bg-muted rounded-md" />
            </div>
          </Card>
          <Card className="p-6">
            <div className="space-y-4">
              <Skeleton className="h-4 w-[180px]" />
              <div className="space-y-2">
                <Skeleton className="h-12 w-full" />
                <Skeleton className="h-12 w-full" />
                <Skeleton className="h-12 w-full" />
              </div>
            </div>
          </Card>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <Alert variant="destructive">
        <AlertCircle className="h-4 w-4" />
        <AlertTitle>Error</AlertTitle>
        <AlertDescription>
          {error}
          <button 
            onClick={() => window.location.reload()}
            className="underline ml-2 hover:text-muted-foreground"
          >
            Try reloading
          </button>
        </AlertDescription>
      </Alert>
    );
  }

  if (!data) {
    return (
      <Alert>
        <AlertCircle className="h-4 w-4" />
        <AlertTitle>No Data</AlertTitle>
        <AlertDescription>
          No environmental analysis data available. Please ensure all required parameters are provided.
        </AlertDescription>
      </Alert>
    );
  }

  const { 
    impact_assessment, 
    consumption_metrics, 
    allocated_impacts, 
    energy_efficiency, 
    resource_depletion, 
    waste_recycling_rate 
  } = data;

  const hasValidData = impact_assessment &&
    consumption_metrics &&
    typeof energy_efficiency === 'number' &&
    typeof resource_depletion === 'number' &&
    typeof waste_recycling_rate === 'number';

  if (!hasValidData) {
    return (
      <Alert>
        <AlertCircle className="h-4 w-4" />
        <AlertTitle>Invalid Data</AlertTitle>
        <AlertDescription>
          The environmental analysis data is incomplete or invalid. Please check the input parameters.
        </AlertDescription>
      </Alert>
    );
  }

  return (
    <div className="space-y-6">
      <div className="grid gap-6 md:grid-cols-2">
        <ImpactMetrics
          impacts={impact_assessment}
          allocatedImpacts={allocated_impacts}
        />
        <SustainabilityScore
          energyEfficiency={energy_efficiency}
          resourceDepletion={resource_depletion}
          wasteRecycling={waste_recycling_rate}
        />
      </div>
      <div className="grid gap-6 md:grid-cols-2">
        <EmissionsBreakdown
          impacts={impact_assessment}
          allocatedImpacts={allocated_impacts}
        />
        <ResourceConsumption
          metrics={consumption_metrics}
          efficiency={energy_efficiency}
        />
      </div>
    </div>
  );
} 