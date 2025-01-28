"use client";

import React, { useState } from 'react';
import { message } from 'antd';
import { useSubmitAnalysis, useAnalysisResults } from '@/hooks/useAnalysis';
import TechnicalAnalysisView from '@/features/analysis/technical/components/TechnicalAnalysisView';
import AnalysisLayout from '@/features/analysis/components/AnalysisLayout';
import TechnicalInputForm from '@/components/forms/TechnicalInputForm';
import { ProcessAnalysis } from '@/types/process';

const steps = [
  {
    title: 'Input Parameters',
    description: 'Enter technical process parameters',
  },
  {
    title: 'Analysis Results',
    description: 'View technical analysis results',
  },
];

export default function TechnicalAnalysisPage() {
  const [currentStep, setCurrentStep] = useState(0);
  const [analysisId, setAnalysisId] = useState<string | null>(null);
  
  const { mutate: submitAnalysis, isPending: isSubmitting } = useSubmitAnalysis();
  const { 
    data: analysisData, 
    isLoading: isLoadingResults,
    error 
  } = useAnalysisResults(analysisId);

  const handleAnalysisComplete = async (values: ProcessAnalysis) => {
    try {
      submitAnalysis(values, {
        onSuccess: (response) => {
          setAnalysisId(response.analysisId);
          setCurrentStep(1);
          message.success('Technical analysis started successfully');
        },
        onError: (error) => {
          message.error(error.message || 'Failed to start analysis');
        }
      });
    } catch (error: any) {
      message.error(error.message || 'An error occurred');
    }
  };

  const loading = isSubmitting || isLoadingResults;
  const loadingText = isSubmitting 
    ? 'Submitting analysis...' 
    : 'Processing technical analysis...';

  return (
    <AnalysisLayout
      title="Technical Analysis"
      currentStep={currentStep}
      steps={steps}
      loading={loading}
      loadingText={loadingText}
    >
      {currentStep === 0 ? (
        <TechnicalInputForm
          onSubmit={handleAnalysisComplete}
          isSubmitting={isSubmitting}
        />
      ) : (
        <>
          {error ? (
            <div className="text-red-500 text-center p-4">
              {error.message || 'An error occurred while processing the analysis'}
            </div>
          ) : (
            analysisData?.results?.technical && (
              <TechnicalAnalysisView data={analysisData.results.technical} />
            )
          )}
        </>
      )}
    </AnalysisLayout>
  );
} 