"use client";

import * as React from "react";
import { Check } from "lucide-react";
import { cn } from "@/lib/utils";

interface StepProps {
  title: string;
  description?: string;
  status: "complete" | "current" | "upcoming";
}

export function Step({ title, description, status }: StepProps) {
  return (
    <div className="flex items-center gap-2">
      <div
        className={cn(
          "flex h-8 w-8 shrink-0 items-center justify-center rounded-full border-2 transition-colors",
          status === "complete"
            ? "border-primary bg-primary text-primary-foreground"
            : status === "current"
              ? "border-primary"
              : "border-input"
        )}
      >
        {status === "complete" ? (
          <Check className="h-4 w-4" />
        ) : (
          <span className="text-sm font-medium">
            {title.charAt(0).toUpperCase()}
          </span>
        )}
      </div>
      <div className="flex flex-col">
        <span
          className={cn(
            "text-sm font-medium",
            status === "complete" && "text-muted-foreground"
          )}
        >
          {title}
        </span>
        {description && (
          <span className="text-sm text-muted-foreground">{description}</span>
        )}
      </div>
    </div>
  );
}

interface StepsProps {
  steps: Array<{
    title: string;
    description?: string;
  }>;
  currentStep: number;
}

export function Steps({ steps, currentStep }: StepsProps) {
  return (
    <div className="flex flex-col gap-4">
      {steps.map((step, index) => (
        <React.Fragment key={step.title}>
          <Step
            title={step.title}
            description={step.description}
            status={
              index + 1 < currentStep
                ? "complete"
                : index + 1 === currentStep
                  ? "current"
                  : "upcoming"
            }
          />
          {index < steps.length - 1 && (
            <div
              className={cn(
                "ml-4 h-8 w-px bg-border",
                index + 1 < currentStep && "bg-primary"
              )}
            />
          )}
        </React.Fragment>
      ))}
    </div>
  );
}
