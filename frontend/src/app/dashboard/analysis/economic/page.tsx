"use client";

import React, { useState } from "react";
import { message } from "antd";
import { useSubmitAnalysis, useAnalysisResults } from "@/hooks/useAnalysis";
import EconomicAnalysisView from "@/features/analysis/economic/components/EconomicAnalysisView";
import AnalysisLayout from "@/features/analysis/components/AnalysisLayout";
import EconomicInputForm from "@/components/forms/EconomicInputForm";

const steps = [
  {
    title: "Input Parameters",
    description: "Enter economic parameters",
  },
  {
    title: "Analysis Results",
    description: "View economic analysis results",
  },
];

export default function EconomicAnalysisPage() {
  const [currentStep, setCurrentStep] = useState(0);
  const [analysisId, setAnalysisId] = useState<string | null>(null);

  const { mutate: submitAnalysis, isLoading: isSubmitting } =
    useSubmitAnalysis();
  const { data: analysisData, error } = useAnalysisResults(analysisId);

  const handleAnalysisComplete = async (values: any) => {
    try {
      submitAnalysis(
        {
          type: "economic",
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
      title="Economic Analysis"
      currentStep={currentStep}
      steps={steps}
      loading={isSubmitting}
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
              {error.message || "An error occurred during analysis"}
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
