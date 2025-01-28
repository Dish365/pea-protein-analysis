"use client";

import React, { useState } from 'react';
import { message } from 'antd';
import { useSubmitAnalysis, useAnalysisResults } from '@/hooks/useAnalysis';
import EnvironmentalAnalysisView from '@/features/analysis/environmental/components/EnvironmentalAnalysisView';
import AnalysisLayout from '@/features/analysis/components/AnalysisLayout';
import EnvironmentalInputForm from '@/components/forms/EnvironmentalInputForm';
import { ProcessAnalysis } from '@/types/process';

const steps = [
  {
    title: 'Input Parameters',
    description: 'Enter environmental parameters',
  },
  {
    title: 'Analysis Results',
    description: 'View environmental impact analysis',
  },
];

export default function EnvironmentalAnalysisPage() {
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
          message.success('Environmental analysis started successfully');
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
    : 'Processing environmental analysis...';

  return (
    <AnalysisLayout
      title="Environmental Analysis"
      currentStep={currentStep}
      steps={steps}
      loading={loading}
      loadingText={loadingText}
    >
      {currentStep === 0 ? (
        <EnvironmentalInputForm
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
            analysisData?.results?.environmental && (
              <EnvironmentalAnalysisView data={analysisData.results.environmental} />
            )
          )}
        </>
      )}
    </AnalysisLayout>
  );
} 