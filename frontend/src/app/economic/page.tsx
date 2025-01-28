"use client";

import React, { useState } from 'react';
import { message } from 'antd';
import { useSubmitAnalysis, useAnalysisResults } from '@/hooks/useAnalysis';
import EconomicAnalysisView from '@/features/analysis/economic/components/EconomicAnalysisView';
import AnalysisLayout from '@/features/analysis/components/AnalysisLayout';
import EconomicInputForm from '@/components/forms/EconomicInputForm';
import { ProcessAnalysis } from '@/types/process';

const steps = [
  {
    title: 'Input Parameters',
    description: 'Enter economic parameters',
  },
  {
    title: 'Analysis Results',
    description: 'View economic analysis results',
  },
];

export default function EconomicAnalysisPage() {
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
          message.success('Economic analysis started successfully');
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
    : 'Processing economic analysis...';

  return (
    <AnalysisLayout
      title="Economic Analysis"
      currentStep={currentStep}
      steps={steps}
      loading={loading}
      loadingText={loadingText}
    >
      {currentStep === 0 ? (
        <EconomicInputForm
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
            analysisData?.results?.economic && (
              <EconomicAnalysisView data={analysisData.results.economic} />
            )
          )}
        </>
      )}
    </AnalysisLayout>
  );
} 