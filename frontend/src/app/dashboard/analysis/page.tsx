"use client";

import React from 'react';
import { Card } from "@/components/ui/card";
import { useAnalysisFlow } from '@/hooks/useAnalysisFlow';
import TechnicalInputForm from '@/components/forms/TechnicalInputForm';
import EconomicInputForm from '@/components/forms/EconomicInputForm';
import EnvironmentalInputForm from '@/components/forms/EnvironmentalInputForm';
import { AnalysisPreview } from '@/components/forms/AnalysisPreview';
import { TechnicalParameters } from "@/types/technical";
import { EconomicParameters } from "@/types/economic";
import { EnvironmentalParameters } from "@/types/environmental";
import { Beaker, Building2, Leaf, ClipboardCheck } from "lucide-react";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { Progress } from "@/components/ui/progress";
import { Button } from "@/components/ui/button";

export const analysisSteps = [
  {
    title: 'Technical Analysis',
    description: 'Configure technical parameters',
    icon: Beaker,
    color: 'text-blue-500'
  },
  {
    title: 'Economic Analysis',
    description: 'Define economic parameters',
    icon: Building2,
    color: 'text-amber-500'
  },
  {
    title: 'Environmental Analysis',
    description: 'Set environmental parameters',
    icon: Leaf,
    color: 'text-emerald-500'
  },
  {
    title: 'Review & Submit',
    description: 'Review and submit analysis',
    icon: ClipboardCheck,
    color: 'text-purple-500'
  }
];

export default function AnalysisPage() {
  const {
    step,
    data,
    errors,
    isSubmitting,
    goToStep,
    handleTechnicalSubmit,
    handleEconomicSubmit,
    handleEnvironmentalSubmit,
    handleSubmitAnalysis
  } = useAnalysisFlow();

  const currentStepIndex = ['technical', 'economic', 'environmental', 'preview'].indexOf(step);
  const currentStep = analysisSteps[currentStepIndex];
  const progress = ((currentStepIndex + (step !== 'preview' && data[step] ? 1 : 0)) / analysisSteps.length) * 100;

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

  const renderCurrentStep = () => {
    switch (step) {
      case 'technical':
        return (
          <div>
            <TechnicalInputForm 
              onSubmit={handleStepChange}
              isSubmitting={isSubmitting}
              initialData={data.technical as TechnicalParameters}
            />
            <div className="mt-6 flex justify-end">
              <Button
                type="submit"
                form="technical-form"
                disabled={isSubmitting}
              >
                Continue
              </Button>
            </div>
          </div>
        );
      
      case 'economic':
        return (
          <div>
            <EconomicInputForm 
              onSubmit={handleStepChange}
              isSubmitting={isSubmitting}
              initialData={data.economic as EconomicParameters}
            />
            <div className="mt-6 flex justify-between">
              <Button
                variant="outline"
                onClick={() => goToStep('technical')}
                disabled={isSubmitting}
              >
                Previous
              </Button>
              <Button
                type="submit"
                form="economic-form"
                disabled={isSubmitting}
              >
                Continue
              </Button>
            </div>
          </div>
        );
      
      case 'environmental':
        return (
          <div>
            <EnvironmentalInputForm 
              onSubmit={handleStepChange}
              isSubmitting={isSubmitting}
              initialData={data.environmental ? {
                ...data.environmental,
                production_volume: data.economic?.production_volume || 0,
                hybrid_weights: data.environmental?.hybrid_weights || {}
              } as EnvironmentalParameters : undefined}
            />
            <div className="mt-6 flex justify-between">
              <Button
                variant="outline"
                onClick={() => goToStep('economic')}
                disabled={isSubmitting}
              >
                Previous
              </Button>
              <Button
                type="submit"
                form="environmental-form"
                disabled={isSubmitting}
              >
                Review
              </Button>
            </div>
          </div>
        );
      
      case 'preview':
        return (
          <AnalysisPreview
            data={data as any}
            onBack={() => goToStep('environmental')}
            onSubmit={async () => {
              const analysisId = await handleSubmitAnalysis();
              if (analysisId) {
                window.location.href = `/dashboard/analysis/results/${analysisId}`;
              }
            }}
            isSubmitting={isSubmitting}
          />
        );
      
      default:
        return null;
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
        
        {/* Current Step Form */}
        <div className="mb-8">
          <h2 className="text-xl font-semibold mb-6">{currentStep?.title}</h2>
          {renderCurrentStep()}
        </div>

        {/* Progress Indicator */}
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