"use client";

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import { Alert, AlertTitle, AlertDescription } from "@/components/ui/alert";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { EnvironmentalInputForm } from '@/components/forms/EnvironmentalInputForm';
import { EnvironmentalAnalysisView } from '@/features/analysis/environmental/components/EnvironmentalAnalysisView';
import { EnvironmentalAnalysisRequest, EnvironmentalAnalysisResponse } from '@/types/environmental';
import { API_ENDPOINTS, API_CONFIG } from '@/config/api';
import { 
  Loader2, AlertCircle, ArrowRight, FileSpreadsheet, Leaf, 
  CheckCircle2, RefreshCcw 
} from 'lucide-react';
import { Progress } from "@/components/ui/progress";
import { MotionDiv } from "@/components/motion";
import { cn } from "@/lib/utils";

export default function EnvironmentalAnalysisPage() {
  const router = useRouter();
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [results, setResults] = useState<EnvironmentalAnalysisResponse | null>(null);
  const [activeTab, setActiveTab] = useState<string>("input");
  const [progress, setProgress] = useState(0);

  const simulateProgress = () => {
    setProgress(0);
    const interval = setInterval(() => {
      setProgress((prev) => {
        if (prev >= 90) {
          clearInterval(interval);
          return prev;
        }
        return prev + 10;
      });
    }, 500);
    return interval;
  };

  const handleSubmit = async (values: EnvironmentalAnalysisRequest) => {
    setIsSubmitting(true);
    setError(null);
    const progressInterval = simulateProgress();

    try {
      const response = await fetch(API_ENDPOINTS.environmental.analyze, {
        method: 'POST',
        ...API_CONFIG,
        body: JSON.stringify(values),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail?.message || 'Failed to perform environmental analysis');
      }

      const data = await response.json();
      setProgress(100);
      await new Promise(resolve => setTimeout(resolve, 500)); // Allow progress to complete
      setResults(data);
      setActiveTab("results");
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An unexpected error occurred');
      setProgress(0);
    } finally {
      setIsSubmitting(false);
      clearInterval(progressInterval);
    }
  };

  const handleReset = () => {
    setResults(null);
    setActiveTab("input");
    setError(null);
  };

  return (
    <>
      {error && (
        <MotionDiv
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -20 }}
          className="mb-6"
        >
          <Alert 
            variant="destructive" 
            className="animate-in fade-in slide-in-from-top-2 duration-300"
          >
            <AlertCircle className="h-4 w-4" />
            <AlertTitle>Analysis Error</AlertTitle>
            <AlertDescription className="mt-2 flex items-center gap-2">
              {error}
              <button 
                onClick={handleReset}
                className="inline-flex items-center gap-1 underline hover:text-destructive-foreground/80"
              >
                <RefreshCcw className="h-3 w-3" />
                Try again
              </button>
            </AlertDescription>
          </Alert>
        </MotionDiv>
      )}

      <Tabs 
        value={activeTab} 
        onValueChange={setActiveTab}
        className="animate-in fade-in duration-500"
      >
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-8">
          <TabsList className="grid w-full sm:w-[400px] grid-cols-2 p-1">
            <TabsTrigger 
              value="input" 
              className={cn(
                "flex items-center gap-2 data-[state=active]:bg-emerald-500 data-[state=active]:text-white",
                "transition-all duration-200"
              )}
              disabled={isSubmitting}
            >
              <FileSpreadsheet className="w-4 h-4" />
              Process Parameters
            </TabsTrigger>
            <TabsTrigger 
              value="results" 
              disabled={!results || isSubmitting}
              className={cn(
                "flex items-center gap-2 data-[state=active]:bg-emerald-500 data-[state=active]:text-white",
                "transition-all duration-200"
              )}
            >
              <Leaf className="w-4 h-4" />
              Impact Assessment
              {results && <ArrowRight className="w-4 h-4 ml-auto" />}
            </TabsTrigger>
          </TabsList>

          {isSubmitting ? (
            <MotionDiv
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              className="flex flex-col gap-2 min-w-[200px]"
            >
              <div className="flex items-center gap-2 text-sm text-muted-foreground">
                <Loader2 className="w-4 h-4 animate-spin" />
                <span>Analyzing Environmental Impact...</span>
              </div>
              <Progress value={progress} className="h-1" />
            </MotionDiv>
          ) : results && (
            <MotionDiv
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              className="flex items-center gap-2"
            >
              <div className="flex items-center gap-2 px-3 py-1.5 bg-emerald-50 dark:bg-emerald-950/30 text-emerald-600 dark:text-emerald-400 rounded-full text-sm border border-emerald-100 dark:border-emerald-900">
                <CheckCircle2 className="w-4 h-4" />
                <span>Analysis Complete</span>
              </div>
              <button
                onClick={handleReset}
                className="p-1.5 hover:bg-muted rounded-full transition-colors"
                aria-label="Reset Analysis"
              >
                <RefreshCcw className="w-4 h-4" />
              </button>
            </MotionDiv>
          )}
        </div>

        <div className="relative">
          <TabsContent 
            value="input"
            className={cn(
              "duration-500",
              activeTab === "input" ? "relative" : "absolute top-0 left-0 w-full"
            )}
          >
            <MotionDiv
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: 20 }}
              className="bg-card rounded-lg border shadow-sm"
            >
              <div className="p-6">
                <EnvironmentalInputForm
                  onSubmit={handleSubmit}
                  isLoading={isSubmitting}
                />
              </div>
            </MotionDiv>
          </TabsContent>

          <TabsContent 
            value="results"
            className={cn(
              "duration-500",
              activeTab === "results" ? "relative" : "absolute top-0 left-0 w-full"
            )}
          >
            {results && (
              <MotionDiv
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: -20 }}
                className="bg-card rounded-lg border shadow-sm"
              >
                <div className="p-6">
                  <EnvironmentalAnalysisView 
                    data={results}
                    error={error || undefined}
                  />
                </div>
              </MotionDiv>
            )}
          </TabsContent>
        </div>
      </Tabs>
    </>
  );
}
