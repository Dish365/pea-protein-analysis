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
  
  // Calculate current step based on both step and data validity
  const currentStepIndex = ['technical', 'economic', 'environmental'].indexOf(step);
  const isCurrentStepValid = data[step] !== undefined;
  
  return (
    <AnalysisLayout
      title="Process Analysis"
      currentStep={isCurrentStepValid ? currentStepIndex : Math.max(0, currentStepIndex - 1)}
      steps={analysisSteps}
      loading={isSubmitting}
      loadingText="Processing analysis..."
      error={errors.length > 0 ? { step, message: errors[0] } : undefined}
    >
      {children}
    </AnalysisLayout>
  );
} 