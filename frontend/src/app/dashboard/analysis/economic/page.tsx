"use client";

import React, { useState } from "react";
import { useSubmitAnalysis, useAnalysisResults } from "@/hooks/useAnalysis";
import { EconomicAnalysisView } from "@/features/analysis/economic/components/EconomicAnalysisView";
import AnalysisLayout from "@/features/analysis/components/AnalysisLayout";
import EconomicInputForm from "@/components/forms/EconomicInputForm";
import { useToast } from "@/hooks/useToast";

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

  const { mutate: submitAnalysis, isPending: isSubmitting } = useSubmitAnalysis();
  const { data: analysisData, error } = useAnalysisResults(analysisId);
  const { toast } = useToast();

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
            <div className="text-destructive text-center p-4">
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
