"use client";

import React from 'react';
import { Card } from "@/components/ui/card";
import { useAnalysisFlow } from '@/hooks/useAnalysisFlow';
import TechnicalAnalysisView from '@/features/analysis/technical/components/TechnicalAnalysisView';
import { EconomicAnalysisView } from '@/features/analysis/economic/components/EconomicAnalysisView';
import { EnvironmentalAnalysisView } from '@/features/analysis/environmental/components/EnvironmentalAnalysisView';
import TechnicalInputForm from '@/components/forms/TechnicalInputForm';
import EconomicInputForm from '@/components/forms/EconomicInputForm';
import EnvironmentalInputForm from '@/components/forms/EnvironmentalInputForm';
import { TechnicalResults } from '@/types/technical';
import { EconomicResults } from '@/types/economic';
import { EnvironmentalResults, EnvironmentalParameters } from '@/types/environmental';
import { Beaker, Building2, Leaf } from "lucide-react";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { Progress } from "@/components/ui/progress";

export const analysisSteps = [
  {
    title: 'Technical Analysis',
    description: 'Configure technical parameters',
    icon: Beaker,
    color: 'text-blue-500'
  },
  {
    title: 'Economic Analysis',
    description: 'Configure economic parameters',
    icon: Building2,
    color: 'text-green-500'
  },
  {
    title: 'Environmental Analysis',
    description: 'Configure environmental parameters',
    icon: Leaf,
    color: 'text-emerald-500'
  }
];

export default function AnalysisPage() {
  const {
    step,
    data,
    errors,
    isSubmitting,
    handleTechnicalSubmit,
    handleEconomicSubmit,
    handleEnvironmentalSubmit
  } = useAnalysisFlow();

  const currentStepIndex = ['technical', 'economic', 'environmental'].indexOf(step);
  const currentStep = analysisSteps[currentStepIndex];
  const progress = ((currentStepIndex + (data[step] ? 1 : 0)) / analysisSteps.length) * 100;

  const handleStepChange = async (stepData: any) => {
    switch (step) {
      case 'technical':
        await handleTechnicalSubmit(stepData);
        break;
      case 'economic':
        await handleEconomicSubmit(stepData);
        break;
      case 'environmental':
        await handleEnvironmentalSubmit(stepData);
        break;
    }
  };

  return (
    <div className="p-6">
      <Card className="p-6">
        {errors.length > 0 && (
          <Alert variant="destructive" className="mb-6">
            <AlertDescription>{errors.join(', ')}</AlertDescription>
          </Alert>
        )}
        
        {step === 'technical' && (
          <TechnicalInputForm 
            onSubmit={handleStepChange}
            isSubmitting={isSubmitting}
            initialData={data.technical}
          />
        )}

        {step === 'economic' && data.technical && (
          <EconomicInputForm 
            onSubmit={handleStepChange}
            isSubmitting={isSubmitting}
            initialData={data.economic}
          />
        )}

        {step === 'environmental' && data.economic && (
          <EnvironmentalInputForm 
            onSubmit={handleStepChange}
            isSubmitting={isSubmitting}
            initialData={data.environmental ? {
              ...data.environmental,
              production_volume: data.economic.production_volume,
              hybrid_weights: data.environmental.hybrid_weights || {}
            } as EnvironmentalParameters : undefined}
          />
        )}

        {data.technical && step !== 'technical' && (
          <TechnicalAnalysisView 
            data={data.technical as unknown as TechnicalResults} 
            isLoading={isSubmitting} 
          />
        )}

        {data.economic && step !== 'economic' && (
          <EconomicAnalysisView 
            data={data.economic as unknown as EconomicResults} 
            isLoading={isSubmitting} 
          />
        )}

        {data.environmental && step !== 'environmental' && (
          <EnvironmentalAnalysisView 
            data={data.environmental as unknown as EnvironmentalResults} 
            isLoading={isSubmitting} 
          />
        )}

        <div className="mt-6 border-t pt-6">
          <div className="flex justify-between items-center">
            <div className="text-sm text-muted-foreground">
              Step {currentStepIndex + 1} of {analysisSteps.length}
            </div>
            <div className="text-sm text-muted-foreground">
              {currentStep?.title}
            </div>
          </div>
          <Progress value={progress} className="mt-2" />
        </div>
      </Card>
    </div>
  );
} 