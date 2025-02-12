"use client";

import React from "react";
import { Steps } from "@/components/ui/steps";
import { LoadingSpinner } from "@/components/ui/loading-spinner";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { ProcessStatus } from "@/types/process";
import { Button } from "@/components/ui/button";
import { ArrowLeft, Save } from "lucide-react";
import { useRouter } from "next/navigation";

interface AnalysisLayoutProps {
  title: string;
  currentStep: number;
  steps: Array<{
    title: string;
    description: string;
    status?: ProcessStatus;
  }>;
  loading?: boolean;
  loadingText?: string;
  error?: string;
  onSave?: () => void;
  children: React.ReactNode;
}

export function AnalysisLayout({
  title,
  currentStep,
  steps,
  loading,
  loadingText = "Processing analysis...",
  error,
  onSave,
  children,
}: AnalysisLayoutProps) {
  const router = useRouter();

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <Button
            variant="ghost"
            size="icon"
            onClick={() => router.back()}
          >
            <ArrowLeft className="h-4 w-4" />
          </Button>
          <h1 className="text-2xl font-semibold">{title}</h1>
        </div>
        {onSave && (
          <Button onClick={onSave}>
            <Save className="mr-2 h-4 w-4" />
            Save Analysis
          </Button>
        )}
      </div>
      
      <Steps
        steps={steps.map(step => ({
          ...step,
          status: step.status || (
            currentStep > steps.indexOf(step)
              ? ProcessStatus.COMPLETED
              : currentStep === steps.indexOf(step)
                ? ProcessStatus.PROCESSING
                : ProcessStatus.PENDING
          )
        }))}
        currentStep={currentStep}
      />

      <div className="mt-8">
        {error ? (
          <Alert variant="destructive">
            <AlertDescription>{error}</AlertDescription>
          </Alert>
        ) : loading ? (
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