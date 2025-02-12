"use client";

import React from 'react';
import { AlertCircle } from 'lucide-react';
import { Alert, AlertDescription } from "@/components/ui/alert";
import { Card } from '@/components/ui/card';
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
      <Card className="p-6">
        <div className="animate-pulse space-y-4">
          <div className="h-4 bg-muted rounded w-1/4" />
          <div className="h-32 bg-muted rounded" />
        </div>
      </Card>
    );
  }

  if (error) {
    return (
      <Alert variant="destructive">
        <AlertCircle className="h-4 w-4" />
        <AlertDescription>{error}</AlertDescription>
      </Alert>
    );
  }

  if (!data) {
    return (
      <Alert>
        <AlertCircle className="h-4 w-4" />
        <AlertDescription>
          No environmental analysis data available
        </AlertDescription>
      </Alert>
    );
  }

  const { impact_assessment, consumption_metrics, allocated_impacts, energy_efficiency, resource_depletion, waste_recycling_rate } = data;

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