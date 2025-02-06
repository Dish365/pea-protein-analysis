"use client";

import React from 'react';
import { Steps, Spin } from 'antd';

interface AnalysisLayoutProps {
  title: string;
  currentStep: number;
  steps: Array<{
    title: string;
    description: string;
  }>;
  loading?: boolean;
  loadingText?: string;
  children: React.ReactNode;
}

export default function AnalysisLayout({
  title,
  currentStep,
  steps,
  loading,
  loadingText,
  children,
}: AnalysisLayoutProps) {
  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-semibold">{title}</h1>
      
      <Steps
        current={currentStep}
        items={steps.map((step, index) => ({
          key: index,
          title: step.title,
          description: step.description,
        }))}
      />

      <div className="mt-8">
        {loading ? (
          <div className="text-center py-12">
            <Spin tip={loadingText} />
          </div>
        ) : (
          children
        )}
      </div>
    </div>
  );
} 