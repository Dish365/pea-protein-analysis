"use client";

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import { Alert, AlertTitle, AlertDescription } from "@/components/ui/alert";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import EconomicInputForm from '@/components/forms/EconomicInputForm';
import { EconomicAnalysisView } from '@/features/analysis/economic/components/EconomicAnalysisView';
import { EconomicFormValues, ComprehensiveAnalysisResponse } from '@/types/economic';
import { API_ENDPOINTS, API_CONFIG } from '@/config/api';
import AnalysisLayout from '@/components/layout/AnalysisLayout';
import { 
  Loader2, AlertCircle, ArrowRight, FileSpreadsheet, BarChart, 
  CheckCircle2, RefreshCcw 
} from 'lucide-react';
import { cn } from '@/lib/utils';
import { AnimatePresence } from 'framer-motion';
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip";
import { Progress } from "@/components/ui/progress";
import { MotionDiv, slideUp, scale, slideInLeft, slideInRight } from "@/components/motion";

export default function AnalysisPage() {
  const router = useRouter();
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [results, setResults] = useState<ComprehensiveAnalysisResponse | null>(null);
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

  const handleSubmit = async (values: EconomicFormValues) => {
    setIsSubmitting(true);
    setError(null);
    const progressInterval = simulateProgress();

    try {
      const response = await fetch(API_ENDPOINTS.economic.analyze, {
        method: 'POST',
        ...API_CONFIG,
        body: JSON.stringify(values),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to perform economic analysis');
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
    }
  };

  const handleReset = () => {
    setResults(null);
    setActiveTab("input");
    setError(null);
  };

  return (
    <AnalysisLayout>
      <AnimatePresence mode="wait">
        {error && (
          <MotionDiv
            {...slideUp}
            className="mb-6"
          >
            <Alert 
              variant="destructive" 
              className="animate-in fade-in slide-in-from-top-2 duration-300"
            >
              <AlertCircle className="h-4 w-4" />
              <AlertTitle>Analysis Error</AlertTitle>
              <AlertDescription className="mt-2 text-sm">
                {error}
                <button 
                  onClick={handleReset}
                  className="ml-2 underline hover:text-destructive-foreground/80"
                >
                  Try again
                </button>
              </AlertDescription>
            </Alert>
          </MotionDiv>
        )}
      </AnimatePresence>

      <Tabs 
        value={activeTab} 
        onValueChange={setActiveTab}
        className="animate-in fade-in duration-500"
      >
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-8">
          <TabsList className="grid w-full sm:w-[400px] grid-cols-2 p-1 relative">
            <TooltipProvider>
              <Tooltip>
                <TooltipTrigger asChild>
                  <TabsTrigger 
                    value="input" 
                    className={cn(
                      "flex items-center gap-2 data-[state=active]:bg-primary data-[state=active]:text-primary-foreground",
                      "transition-all duration-200 relative overflow-hidden"
                    )}
                  >
                    <FileSpreadsheet className="w-4 h-4" />
                    Input Parameters
                    {activeTab === "input" && (
                      <MotionDiv
                        className="absolute inset-0 bg-primary/10"
                        layoutId="tab-background"
                        transition={{ type: "spring", bounce: 0.2, duration: 0.6 }}
                      />
                    )}
                  </TabsTrigger>
                </TooltipTrigger>
                <TooltipContent>
                  <p>Configure economic analysis parameters</p>
                </TooltipContent>
              </Tooltip>

              <Tooltip>
                <TooltipTrigger asChild>
                  <TabsTrigger 
                    value="results" 
                    disabled={!results}
                    className={cn(
                      "flex items-center gap-2 data-[state=active]:bg-primary data-[state=active]:text-primary-foreground",
                      "transition-all duration-200 relative overflow-hidden",
                      !results && "opacity-50 cursor-not-allowed"
                    )}
                  >
                    <BarChart className="w-4 h-4" />
                    Results
                    {results && <ArrowRight className="w-4 h-4 ml-auto" />}
                    {activeTab === "results" && (
                      <MotionDiv
                        className="absolute inset-0 bg-primary/10"
                        layoutId="tab-background"
                        transition={{ type: "spring", bounce: 0.2, duration: 0.6 }}
                      />
                    )}
                  </TabsTrigger>
                </TooltipTrigger>
                <TooltipContent>
                  <p>View analysis results and insights</p>
                </TooltipContent>
              </Tooltip>
            </TooltipProvider>
          </TabsList>

          <AnimatePresence mode="wait">
            {isSubmitting ? (
              <MotionDiv
                {...scale}
                className="flex flex-col gap-2 min-w-[200px]"
              >
                <div className="flex items-center gap-2 text-sm text-muted-foreground">
                  <Loader2 className="w-4 h-4 animate-spin" />
                  <span>Processing Analysis...</span>
                </div>
                <Progress value={progress} className="h-1" />
              </MotionDiv>
            ) : results && (
              <MotionDiv
                {...scale}
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
          </AnimatePresence>
        </div>

        <div className="relative">
          <AnimatePresence mode="wait">
            <TabsContent 
              value="input"
              className={cn(
                "duration-500",
                activeTab === "input" ? "relative" : "absolute top-0 left-0 w-full"
              )}
            >
              <MotionDiv
                {...slideInLeft}
                className="bg-card rounded-lg border shadow-sm"
              >
                <div className="p-6">
                  <EconomicInputForm
                    onSubmit={handleSubmit}
                    isSubmitting={isSubmitting}
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
                  {...slideInRight}
                  className="bg-card rounded-lg border shadow-sm"
                >
                  <div className="p-6">
                    <EconomicAnalysisView data={results} />
                  </div>
                </MotionDiv>
              )}
            </TabsContent>
          </AnimatePresence>
        </div>
      </Tabs>
    </AnalysisLayout>
  );
}
