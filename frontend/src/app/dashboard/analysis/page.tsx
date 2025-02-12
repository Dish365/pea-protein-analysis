"use client";

import React from 'react';
import { useRouter } from 'next/navigation';
import { Card, CardContent } from "@/components/ui/card";
import { Steps } from "@/components/ui/steps";
import { LoadingSpinner } from "@/components/ui/loading-spinner";
import TechnicalInputForm from '@/components/forms/TechnicalInputForm';
import EconomicInputForm from '@/components/forms/EconomicInputForm';
import EnvironmentalInputForm from '@/components/forms/EnvironmentalInputForm';
import { useAnalysisFlow } from '@/hooks/useAnalysisFlow';

const steps = [
  {
    title: 'Technical Parameters',
    description: 'Configure process specifications',
  },
  {
    title: 'Economic Parameters',
    description: 'Define cost and revenue factors',
  },
  {
    title: 'Environmental Parameters',
    description: 'Specify environmental impacts',
  }
];

export default function AnalysisPage() {
  const router = useRouter();
  const {
    state,
    isLoading,
    handleTechnicalSubmit,
    handleEconomicSubmit,
    handleEnvironmentalSubmit
  } = useAnalysisFlow();

  // Get current step index
  const getCurrentStepIndex = () => {
    switch (state.step) {
      case 'technical':
        return 0;
      case 'economic':
        return 1;
      case 'environmental':
        return 2;
      case 'complete':
        return 3;
      default:
        return 0;
    }
  };

  // Redirect to results when complete
  React.useEffect(() => {
    if (state.step === 'complete' && state.id) {
      router.push(`/dashboard/analysis/results/${state.id}`);
    }
  }, [state.step, state.id, router]);

  // Render current step form
  const renderStepContent = () => {
    if (isLoading) {
      return (
        <div className="flex items-center justify-center p-8">
          <LoadingSpinner />
        </div>
      );
    }

    switch (state.step) {
      case 'technical':
        return (
          <TechnicalInputForm
            onSubmit={handleTechnicalSubmit}
            isSubmitting={isLoading}
          />
        );
      case 'economic':
        return (
          <EconomicInputForm
            onSubmit={handleEconomicSubmit}
            isSubmitting={isLoading}
          />
        );
      case 'environmental':
        return (
          <EnvironmentalInputForm
            onSubmit={handleEnvironmentalSubmit}
            isSubmitting={isLoading}
          />
        );
      default:
        return null;
    }
  };

  return (
    <div className="container mx-auto py-6 max-w-4xl">
      <Card>
        <CardContent className="pt-6">
          <Steps
            steps={steps}
            currentStep={getCurrentStepIndex() + 1}
          />
          <div className="mt-8">
            {renderStepContent()}
          </div>
        </CardContent>
      </Card>
    </div>
  );
} 