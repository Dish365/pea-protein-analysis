"use client";

import React from 'react';
import { AlertCircle, Loader2 } from 'lucide-react';
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { TechnicalResults } from '@/types/technical';
import { EfficiencyMetrics } from './EfficiencyMetrics';
import { ProteinRecoveryCard } from './ProteinRecoveryCard';
import { ParticleSizeDisplay } from './ParticleSizeDisplay';
import { Card } from '@/components/ui/card';
import { Skeleton } from '@/components/ui/skeleton';

interface TechnicalAnalysisViewProps {
  data?: TechnicalResults;
  isLoading?: boolean;
  error?: string;
}

export function TechnicalAnalysisView({ 
  data, 
  isLoading, 
  error 
}: TechnicalAnalysisViewProps) {
  if (isLoading) {
    return (
      <div className="space-y-6">
        <div className="grid gap-6 md:grid-cols-2">
          <Card className="p-6">
            <div className="flex items-center space-x-4">
              <Loader2 className="h-4 w-4 animate-spin" />
              <div className="space-y-2">
                <Skeleton className="h-4 w-[200px]" />
                <Skeleton className="h-4 w-[150px]" />
              </div>
            </div>
          </Card>
          <Card className="p-6">
            <div className="space-y-4">
              <Skeleton className="h-4 w-[250px]" />
              <div className="space-y-2">
                <Skeleton className="h-4 w-[200px]" />
                <Skeleton className="h-4 w-[180px]" />
              </div>
            </div>
          </Card>
        </div>
        <Card className="p-6">
          <div className="space-y-4">
            <Skeleton className="h-4 w-[300px]" />
            <div className="h-[200px] bg-muted rounded-md" />
          </div>
        </Card>
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
          No technical analysis data available. Please ensure all required parameters are provided.
        </AlertDescription>
      </Alert>
    );
  }

  const { 
    protein_recovery: proteinRecovery, 
    separation_efficiency: separationEfficiency, 
    process_efficiency: processEfficiency, 
    particle_size_distribution: particleSizeDistribution 
  } = data;

  const hasValidData = proteinRecovery && 
    typeof separationEfficiency === 'number' && 
    typeof processEfficiency === 'number' && 
    particleSizeDistribution;

  if (!hasValidData) {
    return (
      <Alert>
        <AlertCircle className="h-4 w-4" />
        <AlertTitle>Invalid Data</AlertTitle>
        <AlertDescription>
          The technical analysis data is incomplete or invalid. Please check the input parameters.
        </AlertDescription>
      </Alert>
    );
  }

  return (
    <div className="space-y-6">
      <div className="grid gap-6 md:grid-cols-2">
        <ProteinRecoveryCard recovery={proteinRecovery} />
        <EfficiencyMetrics
          separationEfficiency={separationEfficiency}
          processEfficiency={processEfficiency}
          proteinYield={proteinRecovery.yield}
        />
      </div>
      <ParticleSizeDisplay distribution={particleSizeDistribution} />
    </div>
  );
}

export default TechnicalAnalysisView; 