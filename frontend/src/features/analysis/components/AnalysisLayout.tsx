"use client";

import React from 'react';
import { Card, Steps } from 'antd';
import LoadingSpinner from '@/components/shared/LoadingSpinner';

const { Step } = Steps;

interface AnalysisLayoutProps {
  title: string;
  currentStep: number;
  loading?: boolean;
  loadingText?: string;
  progress?: number;
  steps: Array<{
    title: string;
    description: string;
  }>;
  children: React.ReactNode;
}

export const AnalysisLayout: React.FC<AnalysisLayoutProps> = ({
  title,
  currentStep,
  loading = false,
  loadingText,
  progress,
  steps,
  children,
}) => {
  return (
    <div className="analysis-pipeline">
      <Card title={title} className="mb-6">
        <Steps current={currentStep} className="analysis-steps">
          {steps.map(item => (
            <Step 
              key={item.title} 
              title={item.title} 
              description={item.description} 
            />
          ))}
        </Steps>

        <div className="analysis-content mt-6">
          {loading ? (
            <LoadingSpinner 
              tip={loadingText || 'Processing analysis...'}
            />
          ) : (
            children
          )}
        </div>
      </Card>
    </div>
  );
};

export default AnalysisLayout; 