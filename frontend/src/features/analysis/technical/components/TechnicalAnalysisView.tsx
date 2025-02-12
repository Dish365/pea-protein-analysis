"use client";

import React from 'react';
import { AlertCircle } from 'lucide-react';
import { Alert, AlertDescription } from "@/components/ui/alert";
import { TechnicalResults } from '@/types/technical';
import { EfficiencyMetrics } from './EfficiencyMetrics';
import { ProteinRecoveryCard } from './ProteinRecoveryCard';
import { ParticleSizeDisplay } from './ParticleSizeDisplay';
import { Card } from '@/components/ui/card';

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
          No technical analysis data available
        </AlertDescription>
      </Alert>
    );
  }

  const { proteinRecovery, separationEfficiency, processEfficiency, particleSizeDistribution } = data;

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