"use client";

import React from "react";
import { Steps } from "@/components/ui/steps";
import { LoadingSpinner } from "@/components/ui/loading-spinner";

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

export function AnalysisLayout({
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
        steps={steps}
        currentStep={currentStep}
      />

      <div className="mt-8">
        {loading ? (
          <div className="flex justify-center py-12">
            <LoadingSpinner tip={loadingText} />
          </div>
        ) : (
          children
        )}
      </div>
    </div>
  );
} 