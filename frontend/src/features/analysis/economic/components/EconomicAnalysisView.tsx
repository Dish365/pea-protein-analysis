"use client";

import React from 'react';
import { AlertCircle, Loader2 } from 'lucide-react';
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { Card } from '@/components/ui/card';
import { Skeleton } from '@/components/ui/skeleton';
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
      <div className="space-y-6">
        <div className="grid gap-6 md:grid-cols-2">
          <Card className="p-6">
            <div className="space-y-4">
              <div className="flex items-center space-x-4">
                <Loader2 className="h-4 w-4 animate-spin" />
                <Skeleton className="h-4 w-[200px]" />
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Skeleton className="h-4 w-[120px]" />
                  <Skeleton className="h-8 w-[150px]" />
                </div>
                <div className="space-y-2">
                  <Skeleton className="h-4 w-[140px]" />
                  <Skeleton className="h-8 w-[130px]" />
                </div>
              </div>
              <div className="h-[150px] bg-muted rounded-md" />
            </div>
          </Card>
          <Card className="p-6">
            <div className="space-y-4">
              <Skeleton className="h-4 w-[250px]" />
              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Skeleton className="h-4 w-[100px]" />
                  <Skeleton className="h-8 w-[140px]" />
                </div>
                <div className="space-y-2">
                  <Skeleton className="h-4 w-[110px]" />
                  <Skeleton className="h-8 w-[120px]" />
                </div>
              </div>
              <div className="h-[150px] bg-muted rounded-md" />
            </div>
          </Card>
        </div>
        <Card className="p-6">
          <div className="space-y-4">
            <Skeleton className="h-4 w-[280px]" />
            <div className="grid grid-cols-3 gap-4">
              <Skeleton className="h-[200px] w-full" />
              <Skeleton className="h-[200px] w-full" />
              <Skeleton className="h-[200px] w-full" />
            </div>
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
          No economic analysis data available. Please ensure all required parameters are provided.
        </AlertDescription>
      </Alert>
    );
  }

  const { 
    capex_analysis, 
    opex_analysis, 
    profitability_analysis, 
    cost_breakdown, 
    unit_production_cost 
  } = data;

  const hasValidData = capex_analysis &&
    opex_analysis &&
    profitability_analysis &&
    cost_breakdown &&
    typeof unit_production_cost === 'number';

  if (!hasValidData) {
    return (
      <Alert>
        <AlertCircle className="h-4 w-4" />
        <AlertTitle>Invalid Data</AlertTitle>
        <AlertDescription>
          The economic analysis data is incomplete or invalid. Please check the input parameters.
        </AlertDescription>
      </Alert>
    );
  }

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