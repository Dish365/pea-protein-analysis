"use client";

import React, { useState } from 'react';
import { Card, Steps, message, Spin, Form } from 'antd';
import EnvironmentalInputForm from '../../components/forms/EnvironmentalInputForm';
import EnvironmentalAnalysis from '../../components/analysis/environmental/page';
import { ProcessAnalysis } from '../../types/process';
import { ENDPOINTS } from '../../config/endpoints';
import axios from 'axios';
import AnalysisLayout from '../../components/layout/AnalysisLayout';

const { Step } = Steps;

const EnvironmentalAnalysisPipeline: React.FC = () => {
  const [currentStep, setCurrentStep] = useState(0);
  const [loading, setLoading] = useState(false);
  const [analysisData, setAnalysisData] = useState<ProcessAnalysis | undefined>();
  const [form] = Form.useForm();

  const steps = [
    {
      title: 'Environmental Parameters',
      description: 'Enter environmental process parameters',
    },
    {
      title: 'Environmental Analysis',
      description: 'View environmental impact results',
    },
  ];

  const handleAnalysisComplete = async (response: any) => {
    try {
      setLoading(true);
      
      // Poll for analysis results
      const result = await pollAnalysisResults(response.analysisId);
      
      setAnalysisData(result);
      setCurrentStep(1);
      message.success('Environmental analysis completed successfully');
    } catch (error: any) {
      message.error(error.message || 'Failed to retrieve analysis results');
    } finally {
      setLoading(false);
    }
  };

  const pollAnalysisResults = async (analysisId: string): Promise<ProcessAnalysis> => {
    const maxAttempts = 30; // 30 seconds timeout
    let attempts = 0;

    while (attempts < maxAttempts) {
      try {
        const response = await axios.get(
          `${ENDPOINTS.PROCESS.RESULTS(parseInt(analysisId))}`
        );

        if (response.data.status === 'completed') {
          return response.data.results;
        }

        if (response.data.status === 'failed') {
          throw new Error('Analysis failed: ' + response.data.error);
        }

        // Wait 1 second before next poll
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
      <div className="environmental-analysis-pipeline">
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
              <div className="loading-container" style={{ textAlign: 'center', padding: '40px' }}>
                <Spin size="large" tip="Processing analysis..." />
              </div>
            ) : currentStep === 0 ? (
              <EnvironmentalInputForm
                form={form}
                onSuccess={handleAnalysisComplete}
                loading={loading}
              />
            ) : (
              <EnvironmentalAnalysis
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

export default EnvironmentalAnalysisPipeline; 