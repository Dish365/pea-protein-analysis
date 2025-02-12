"use client";

import React, { useState } from "react";
import { useSubmitAnalysis, useAnalysisResults } from "@/hooks/useAnalysis";
import { EnvironmentalAnalysisView } from "@/features/analysis/environmental/components/EnvironmentalAnalysisView";
import AnalysisLayout from "@/features/analysis/components/AnalysisLayout";
import EnvironmentalInputForm from "@/components/forms/EnvironmentalInputForm";
import { useToast } from "@/hooks/useToast";

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

  const { mutate: submitAnalysis, isPending: isSubmitting } = useSubmitAnalysis();
  const { data: analysisData, error } = useAnalysisResults(analysisId);
  const { toast } = useToast();

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
            <div className="text-destructive text-center p-4">
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
