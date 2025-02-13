"use client";

import React from "react";
import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import { ArrowLeft, ChevronRight, Check, Circle, Loader2, AlertCircle, LucideIcon } from "lucide-react";
import Link from "next/link";
import { Progress } from "@/components/ui/progress";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";

interface AnalysisStep {
  title: string;
  description: string;
  icon: React.ElementType;
  color: string;
}

interface AnalysisLayoutProps {
  children: React.ReactNode;
  title: string;
  currentStep: number;
  steps: {
    title: string;
    description: string;
    icon: LucideIcon;
    color: string;
  }[];
  loading: boolean;
  loadingText: string;
  error?: {
    step: string;
    message: string;
  };
}

export function AnalysisLayout({
  children,
  title,
  currentStep,
  steps,
  loading,
  loadingText,
  error
}: AnalysisLayoutProps) {
  return (
    <div className="flex h-screen">
      <div className="w-64 border-r bg-muted/10 p-6">
        <div className="space-y-4">
          <div className="flex items-center gap-2">
            <h2 className="text-lg font-semibold">{title}</h2>
            {loading && (
              <Loader2 className="h-4 w-4 animate-spin text-muted-foreground" />
            )}
          </div>
          <Progress value={(currentStep + 1) / steps.length * 100} className="h-2" />
          <nav className="space-y-2">
            {steps.map((step, index) => {
              const isActive = index === currentStep;
              const isComplete = index < currentStep;
              const hasError = error?.step === step.title.toLowerCase();

              return (
                <div
                  key={step.title}
                  className={cn(
                    "flex items-center gap-3 rounded-lg px-3 py-2 text-sm",
                    isActive
                      ? "bg-accent text-accent-foreground"
                      : "text-muted-foreground hover:bg-accent/50 hover:text-accent-foreground",
                    isComplete && "text-foreground",
                    hasError && "border-destructive"
                  )}
                >
                  <step.icon className={cn("h-4 w-4", step.color)} />
                  <div className="flex-1">
                    <div className="font-medium leading-none">{step.title}</div>
                    <div className="text-xs text-muted-foreground">
                      {step.description}
                    </div>
                  </div>
                  {isComplete ? (
                    <Check className="h-4 w-4" />
                  ) : hasError ? (
                    <AlertCircle className="h-4 w-4 text-destructive" />
                  ) : null}
                </div>
              );
            })}
          </nav>
        </div>
      </div>
      <div className="flex-1 overflow-auto">
        {error && (
          <Alert variant="destructive" className="m-6">
            <AlertCircle className="h-4 w-4" />
            <AlertTitle>Error</AlertTitle>
            <AlertDescription>{error.message}</AlertDescription>
          </Alert>
        )}
        {loading ? (
          <div className="flex h-[calc(100vh-2rem)] items-center justify-center">
            <div className="text-center">
              <Loader2 className="mx-auto h-8 w-8 animate-spin text-muted-foreground" />
              <p className="mt-2 text-sm text-muted-foreground">{loadingText}</p>
            </div>
          </div>
        ) : (
          children
        )}
      </div>
    </div>
  );
} 