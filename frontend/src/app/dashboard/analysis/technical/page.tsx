"use client";

import React, { useState } from "react";
import { message } from "antd";
import { useSubmitAnalysis, useAnalysisResults } from "@/hooks/useAnalysis";
import TechnicalAnalysisView from "@/features/analysis/technical/components/TechnicalAnalysisView";
import AnalysisLayout from "@/features/analysis/components/AnalysisLayout";
import TechnicalInputForm from "@/components/forms/TechnicalInputForm";

const steps = [
  {
    title: "Input Parameters",
    description: "Enter technical process parameters",
  },
  {
    title: "Analysis Results",
    description: "View technical analysis results",
  },
];

export default function TechnicalAnalysisPage() {
  const [currentStep, setCurrentStep] = useState(0);
  const [analysisId, setAnalysisId] = useState<string | null>(null);

  const { mutate: submitAnalysis, isLoading: isSubmitting } =
    useSubmitAnalysis();
  const { data: analysisData, error } = useAnalysisResults(analysisId);

  const handleAnalysisComplete = async (values: any) => {
    try {
      submitAnalysis(
        {
          type: "technical",
          parameters: values,
        },
        {
          onSuccess: (data) => {
            setAnalysisId(data.analysisId);
            setCurrentStep(1);
            message.success("Analysis started successfully");
          },
          onError: (error) => {
            message.error("Failed to start analysis");
          },
        }
      );
    } catch (error) {
      message.error("Failed to submit analysis");
    }
  };

  return (
    <AnalysisLayout
      title="Technical Analysis"
      currentStep={currentStep}
      steps={steps}
      loading={isSubmitting}
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
              {error.message || "An error occurred during analysis"}
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
