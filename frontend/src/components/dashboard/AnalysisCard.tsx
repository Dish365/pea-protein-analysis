"use client";

import React from "react";
import { TrendingUp, TrendingDown } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from "@/components/ui/tooltip";
import { cn } from "@/lib/utils";

interface AnalysisCardProps {
  title: string;
  description: string;
  icon: React.ReactNode;
  variant: "default" | "destructive" | "success" | "warning";
  metrics: {
    completed: number;
    inProgress: number;
    trend?: number; // Percentage change from last period
  };
  onClick: () => void;
}

const variantStyles = {
  default: {
    border: "border-primary",
    background: "bg-primary/10",
    text: "text-primary",
    button: "bg-primary hover:bg-primary/90",
  },
  destructive: {
    border: "border-destructive",
    background: "bg-destructive/10",
    text: "text-destructive",
    button: "bg-destructive hover:bg-destructive/90",
  },
  success: {
    border: "border-emerald-500",
    background: "bg-emerald-500/10",
    text: "text-emerald-500",
    button: "bg-emerald-500 hover:bg-emerald-500/90",
  },
  warning: {
    border: "border-yellow-500",
    background: "bg-yellow-500/10",
    text: "text-yellow-500",
    button: "bg-yellow-500 hover:bg-yellow-500/90",
  },
} as const;

export function AnalysisCard({
  title,
  description,
  icon,
  variant = "default",
  metrics,
  onClick,
}: AnalysisCardProps) {
  const totalAnalyses = metrics.completed + metrics.inProgress;
  const completionRate =
    totalAnalyses > 0 ? (metrics.completed / totalAnalyses) * 100 : 0;
  const styles = variantStyles[variant];

  return (
    <Card className={cn("h-full border-t-2", styles.border)}>
      <CardHeader>
        <div className="flex items-start gap-4">
          <div className={cn("p-2 rounded-lg", styles.background)}>{icon}</div>
          <div>
            <CardTitle>{title}</CardTitle>
            <CardDescription>{description}</CardDescription>
          </div>
        </div>
      </CardHeader>
      <CardContent className="space-y-6">
        <TooltipProvider>
          <Tooltip>
            <TooltipTrigger asChild>
              <div>
                <Progress
                  value={completionRate}
                  className={cn("h-2", styles.background)}
                />
              </div>
            </TooltipTrigger>
            <TooltipContent>
              <p>Analysis completion rate: {Math.round(completionRate)}%</p>
            </TooltipContent>
          </Tooltip>
        </TooltipProvider>

        <div className="grid grid-cols-2 gap-4">
          <div>
            <p className="text-sm text-muted-foreground">Completed</p>
            <p className={cn("text-2xl font-semibold", styles.text)}>
              {metrics.completed}
            </p>
          </div>
          <div>
            <p className="text-sm text-muted-foreground">In Progress</p>
            <p className="text-2xl font-semibold text-yellow-500">
              {metrics.inProgress}
            </p>
          </div>
        </div>

        {metrics.trend !== undefined && (
          <div>
            <p className="text-sm text-muted-foreground">Trend</p>
            <div className="flex items-center gap-2">
              {metrics.trend > 0 ? (
                <TrendingUp className="text-emerald-500" />
              ) : (
                <TrendingDown className="text-destructive" />
              )}
              <p
                className={cn(
                  "text-2xl font-semibold",
                  metrics.trend > 0 ? "text-emerald-500" : "text-destructive"
                )}
              >
                {metrics.trend}%
              </p>
            </div>
          </div>
        )}
      </CardContent>
      <CardFooter>
        <Button
          className={cn("w-full text-primary-foreground", styles.button)}
          onClick={onClick}
        >
          Start New Analysis
        </Button>
      </CardFooter>
    </Card>
  );
}
