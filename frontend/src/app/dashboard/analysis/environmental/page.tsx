"use client";

import React, { useState } from "react";
import { message } from "antd";
import { useSubmitAnalysis, useAnalysisResults } from "@/hooks/useAnalysis";
import EnvironmentalAnalysisView from "@/features/analysis/environmental/components/EnvironmentalAnalysisView";
import AnalysisLayout from "@/features/analysis/components/AnalysisLayout";
import EnvironmentalInputForm from "@/components/forms/EnvironmentalInputForm";

const steps = [
  {
    title: "Input Parameters",
    description: "Enter environmental parameters",
  },
  {
    title: "Analysis Results",
    description: "View environmental analysis results",
  },
];

export default function EnvironmentalAnalysisPage() {
  const [currentStep, setCurrentStep] = useState(0);
  const [analysisId, setAnalysisId] = useState<string | null>(null);

  const { mutate: submitAnalysis, isLoading: isSubmitting } =
    useSubmitAnalysis();
  const { data: analysisData, error } = useAnalysisResults(analysisId);

  const handleAnalysisComplete = async (values: any) => {
    try {
      submitAnalysis(
        {
          type: "environmental",
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
      title="Environmental Analysis"
      currentStep={currentStep}
      steps={steps}
      loading={isSubmitting}
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
              {error.message || "An error occurred during analysis"}
            </div>
          ) : (
            analysisData?.results?.environmental && (
              <EnvironmentalAnalysisView
                data={analysisData.results.environmental}
              />
            )
          )}
        </>
      )}
    </AnalysisLayout>
  );
}
