"use client";

import React from 'react';
import { AnalysisLayout } from '@/components/layout/AnalysisLayout';
import { useAnalysisFlow } from '@/hooks/useAnalysisFlow';
import { analysisSteps } from './page';

interface AnalysisPageLayoutProps {
  children: React.ReactNode;
}

export default function AnalysisPageLayout({ children }: AnalysisPageLayoutProps) {
  const { step, data, errors, isSubmitting } = useAnalysisFlow();
  
  // Calculate current step based on completed steps
  const currentStepIndex = ['technical', 'economic', 'environmental'].indexOf(step);
  const previousStep = currentStepIndex > 0 ? ['technical', 'economic', 'environmental'][currentStepIndex - 1] as keyof typeof data : null;
  const isPreviousStepValid = previousStep ? data[previousStep] !== undefined : true;
  
  return (
    <AnalysisLayout
      title="Process Analysis"
      currentStep={currentStepIndex}
      steps={analysisSteps}
      loading={isSubmitting}
      loadingText="Processing analysis..."
      error={errors.length > 0 ? { step, message: errors[0] } : undefined}
    >
      {children}
    </AnalysisLayout>
  );
} 