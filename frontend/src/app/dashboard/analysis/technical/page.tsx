"use client";

import React, { useState } from "react";
import { useSubmitAnalysis, useAnalysisResults } from "@/hooks/useAnalysis";
import { TechnicalAnalysisView } from "@/features/analysis/technical/components/TechnicalAnalysisView";
import AnalysisLayout from "@/features/analysis/components/AnalysisLayout";
import TechnicalInputForm from "@/components/forms/TechnicalInputForm";
import { useToast } from "@/hooks/useToast";

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

  const { mutate: submitAnalysis, isPending: isSubmitting } = useSubmitAnalysis();
  const { data: analysisData, error } = useAnalysisResults(analysisId);
  const { toast } = useToast();

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
            toast({
              title: "Success",
              description: "Analysis started successfully",
            });
          },
          onError: (error) => {
            toast({
              title: "Error",
              description: "Failed to start analysis",
              variant: "destructive",
            });
          },
        }
      );
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to submit analysis",
        variant: "destructive",
      });
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
            <div className="text-destructive text-center p-4">
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
