"use client";

import React from 'react';
import { AlertCircle } from 'lucide-react';
import { Alert, AlertDescription } from "@/components/ui/alert";
import { Card } from '@/components/ui/card';
import { EconomicResults } from '@/types/economic';
import { CostBreakdown } from './CostBreakdown';
import { ProfitabilityMetrics } from './ProfitabilityMetrics';
import { SensitivityAnalysis } from './SensitivityAnalysis';

interface EconomicAnalysisViewProps {
  data?: EconomicResults;
  isLoading?: boolean;
  error?: string;
}

export function EconomicAnalysisView({
  data,
  isLoading,
  error
}: EconomicAnalysisViewProps) {
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
          No economic analysis data available
        </AlertDescription>
      </Alert>
    );
  }

  const { capex_analysis, opex_analysis, profitability_analysis, cost_breakdown, unit_production_cost } = data;

  return (
    <div className="space-y-6">
      <div className="grid gap-6 md:grid-cols-2">
        <CostBreakdown
          capex={capex_analysis}
          opex={opex_analysis}
          costBreakdown={cost_breakdown}
          unitCost={unit_production_cost}
        />
        <ProfitabilityMetrics
          metrics={profitability_analysis}
        />
      </div>
      <SensitivityAnalysis
        npv={profitability_analysis.npv}
        capex={capex_analysis}
        opex={opex_analysis}
      />
    </div>
  );
}