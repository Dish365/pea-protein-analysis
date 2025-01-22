"use client";

import React, { useState } from 'react';
import { Card, Steps, message, Spin } from 'antd';
import ProcessInputForm from '../../components/forms';
import TechnicalAnalysis from '../../components/analysis/technical/page';
import { ProcessAnalysis } from '../../types/process';
import { ENDPOINTS } from '../../config/endpoints';
import axios from 'axios';
import AnalysisLayout from '../../components/layout/AnalysisLayout';
import LoadingState from '../../components/common/LoadingState';

const { Step } = Steps;

const TechnicalAnalysisPipeline: React.FC = () => {
  const [currentStep, setCurrentStep] = useState(0);
  const [loading, setLoading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [analysisData, setAnalysisData] = useState<ProcessAnalysis | undefined>();

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

  const handleAnalysisComplete = async (response: any) => {
    try {
      setLoading(true);
      
      // Poll for analysis results
      const result = await pollAnalysisResults(response.analysisId);
      
      setAnalysisData(result);
      setCurrentStep(1);
      message.success('Technical analysis completed successfully');
    } catch (error: any) {
      message.error(error.message || 'Failed to retrieve analysis results');
    } finally {
      setLoading(false);
    }
  };

  const pollAnalysisResults = async (analysisId: string): Promise<ProcessAnalysis> => {
    const maxAttempts = 30;
    let attempts = 0;

    while (attempts < maxAttempts) {
      try {
        setProgress(Math.min((attempts / maxAttempts) * 100, 95));
        const response = await axios.get(
          `${ENDPOINTS.PROCESS.RESULTS(parseInt(analysisId))}`
        );

        if (response.data.status === 'completed') {
          setProgress(100);
          return response.data.results;
        }

        if (response.data.status === 'failed') {
          throw new Error('Analysis failed: ' + response.data.error);
        }

        await new Promise(resolve => setTimeout(resolve, 1000));
        attempts++;
      } catch (error) {
        throw new Error('Failed to retrieve analysis results');
      }
    }

    throw new Error('Analysis timed out');
  };

  return (
    <AnalysisLayout>
      <div className="technical-analysis-pipeline">
        <Card>
          <Steps current={currentStep} className="analysis-steps">
            {steps.map(item => (
              <Step 
                key={item.title} 
                title={item.title} 
                description={item.description} 
              />
            ))}
          </Steps>

          <div className="analysis-content" style={{ marginTop: '24px' }}>
            {loading ? (
              <LoadingState
                tip="Processing technical analysis..."
                progress={progress}
                subTip={`Analyzing process data (${Math.round(progress)}%)`}
              />
            ) : currentStep === 0 ? (
              <ProcessInputForm
                onSuccess={handleAnalysisComplete}
                loading={loading}
              />
            ) : (
              <TechnicalAnalysis
                data={analysisData}
                loading={loading}
              />
            )}
          </div>
        </Card>
      </div>
    </AnalysisLayout>
  );
};

export default TechnicalAnalysisPipeline; 