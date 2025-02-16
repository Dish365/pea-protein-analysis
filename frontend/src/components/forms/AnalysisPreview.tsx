"use client";

import React from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { ProcessValidationData } from "@/types/process";
import { ArrowLeft, Loader2 } from "lucide-react";

interface AnalysisPreviewProps {
  data: ProcessValidationData;
  onBack: () => void;
  onSubmit: () => void;
  isSubmitting: boolean;
}

export function AnalysisPreview({
  data,
  onBack,
  onSubmit,
  isSubmitting
}: AnalysisPreviewProps) {
  const renderSection = (title: string, data: Record<string, any>) => {
    return (
      <Card className="mb-6">
        <CardHeader>
          <CardTitle className="text-lg">{title}</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-2 gap-4">
            {Object.entries(data).map(([key, value]) => {
              // Skip complex objects and arrays
              if (typeof value === 'object' || Array.isArray(value)) return null;
              
              return (
                <div key={key} className="flex flex-col">
                  <span className="text-sm font-medium text-muted-foreground">
                    {key.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ')}
                  </span>
                  <span className="text-sm">{value}</span>
                </div>
              );
            })}
          </div>
        </CardContent>
      </Card>
    );
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold">Review Analysis Parameters</h2>
        <div className="space-x-4">
          <Button
            variant="outline"
            onClick={onBack}
            disabled={isSubmitting}
          >
            <ArrowLeft className="mr-2 h-4 w-4" />
            Back
          </Button>
          <Button
            onClick={onSubmit}
            disabled={isSubmitting}
          >
            {isSubmitting ? (
              <>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                Submitting...
              </>
            ) : (
              'Submit Analysis'
            )}
          </Button>
        </div>
      </div>

      {renderSection('Technical Parameters', data.technical)}
      {renderSection('Economic Parameters', data.economic)}
      {renderSection('Environmental Parameters', data.environmental)}
    </div>
  );
} 