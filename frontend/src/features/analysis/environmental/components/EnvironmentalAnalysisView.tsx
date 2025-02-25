"use client";

import React from 'react';
import { AlertCircle, Loader2, RefreshCcw } from 'lucide-react';
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { Card } from '@/components/ui/card';
import { Skeleton } from '@/components/ui/skeleton';
import { 
  EnvironmentalAnalysisResponse,
  ImpactResults,
  AllocationResults,
} from '@/types/environmental';
import { EmissionsBreakdown } from './EmissionsBreakdown';
import { ImpactMetrics } from './ImpactMetrics';
import { ResourceConsumption } from './ResourceConsumption';
import { SustainabilityScore } from './SustainabilityScore';
import { MotionDiv } from "@/components/motion";

interface EnvironmentalAnalysisViewProps {
  data?: EnvironmentalAnalysisResponse;
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
      <div className="space-y-8">
        <MotionDiv
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          <Card className="p-6 border-none shadow-lg bg-gradient-to-br from-background to-muted/10">
            <div className="space-y-4">
              <div className="flex items-center space-x-4">
                <Loader2 className="h-4 w-4 animate-spin text-emerald-500" />
                <div className="space-y-2">
                  <Skeleton className="h-4 w-[200px]" />
                  <Skeleton className="h-4 w-[150px]" />
                </div>
              </div>
              <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
                {[1, 2, 3].map((i) => (
                  <Skeleton key={i} className="h-32 rounded-lg" />
                ))}
              </div>
            </div>
          </Card>
        </MotionDiv>
        
        {[1, 2, 3].map((i) => (
          <MotionDiv
            key={i}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: i * 0.1 }}
          >
            <Card className="p-6 border-none shadow-lg bg-gradient-to-br from-background to-muted/10">
              <div className="space-y-4">
                <Skeleton className="h-4 w-[180px]" />
                <div className="space-y-2">
                  <Skeleton className="h-[200px] rounded-lg" />
                </div>
              </div>
            </Card>
          </MotionDiv>
        ))}
      </div>
    );
  }

  if (error) {
    return (
      <MotionDiv
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.3 }}
      >
        <Alert variant="destructive">
          <AlertCircle className="h-4 w-4" />
          <AlertTitle>Error</AlertTitle>
          <AlertDescription className="mt-2 flex items-center gap-2">
            {error}
            <button 
              onClick={() => window.location.reload()}
              className="inline-flex items-center gap-1 underline hover:text-destructive-foreground/80"
            >
              <RefreshCcw className="h-3 w-3" />
              Try reloading
            </button>
          </AlertDescription>
        </Alert>
      </MotionDiv>
    );
  }

  if (!data) {
    return (
      <MotionDiv
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.3 }}
      >
        <Alert>
          <AlertCircle className="h-4 w-4" />
          <AlertTitle>No Data</AlertTitle>
          <AlertDescription>
            No environmental analysis data available. Please ensure all required parameters are provided.
          </AlertDescription>
        </Alert>
      </MotionDiv>
    );
  }

  const { 
    impact_results,
    allocation_results,
    rf_validation,
  } = data;

  const hasValidData = impact_results &&
    typeof impact_results.total_impacts.gwp === 'number' &&
    typeof impact_results.total_impacts.hct === 'number' &&
    typeof impact_results.total_impacts.frs === 'number' &&
    typeof impact_results.total_impacts.water_consumption === 'number' &&
    impact_results.process_contributions &&
    impact_results.metadata &&
    allocation_results &&
    allocation_results.allocation_factors &&
    allocation_results.allocated_impacts;

  if (!hasValidData) {
    return (
      <MotionDiv
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.3 }}
      >
        <Alert>
          <AlertCircle className="h-4 w-4" />
          <AlertTitle>Invalid Data</AlertTitle>
          <AlertDescription>
            The environmental analysis data is incomplete or invalid. Please check the input parameters.
          </AlertDescription>
        </Alert>
      </MotionDiv>
    );
  }

  return (
    <div className="space-y-8">
      <MotionDiv
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <ImpactMetrics
          impactResults={impact_results}
          allocationResults={allocation_results}
        />
      </MotionDiv>

      <MotionDiv
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.1 }}
      >
        <SustainabilityScore
          impactResults={impact_results}
        />
      </MotionDiv>

      <MotionDiv
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.2 }}
      >
        <EmissionsBreakdown
          impactResults={impact_results}
          allocationResults={allocation_results}
        />
      </MotionDiv>

      <MotionDiv
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.3 }}
      >
        <ResourceConsumption
          impactResults={impact_results}
        />
      </MotionDiv>
    </div>
  );
} 