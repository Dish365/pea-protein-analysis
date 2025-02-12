"use client";

import React from 'react';
import { AlertCircle } from 'lucide-react';
import { Alert, AlertDescription } from "@/components/ui/alert";
import { TechnicalResults } from '@/types/technical';
import { EfficiencyMetrics } from './EfficiencyMetrics';
import { ProteinRecoveryCard } from './ProteinRecoveryCard';

interface TechnicalAnalysisViewProps {
  data: TechnicalResults;
}

export function TechnicalAnalysisView({ data }: TechnicalAnalysisViewProps) {
  // Early return if no data
  if (!data) {
    return (
      <Alert variant="warning">
        <AlertCircle className="h-4 w-4" />
        <AlertDescription>
          No technical analysis data available
        </AlertDescription>
      </Alert>
    );
  }

  // Extract efficiency metrics
  const efficiencyMetrics = {
    massEfficiency: data.efficiency,
    processEfficiency: data.yieldRate,
    separationEfficiency: data.qualityScore,
    proteinYield: data.proteinRecovery
  };

  // Extract protein recovery metrics
  const proteinRecovery = {
    massRecovery: data.efficiency,
    contentRecovery: data.qualityScore,
    yieldRecovery: data.proteinRecovery
  };

  return (
    <div className="space-y-6">
      <div className="grid gap-6 md:grid-cols-2">
        <ProteinRecoveryCard
          massRecovery={proteinRecovery.massRecovery}
          contentRecovery={proteinRecovery.contentRecovery}
          yieldRecovery={proteinRecovery.yieldRecovery}
        />
        <EfficiencyMetrics
          massEfficiency={efficiencyMetrics.massEfficiency}
          processEfficiency={efficiencyMetrics.processEfficiency}
          separationEfficiency={efficiencyMetrics.separationEfficiency}
          proteinYield={efficiencyMetrics.proteinYield}
        />
      </div>
    </div>
  );
}

export default TechnicalAnalysisView; 