"use client";

import React from 'react';
import { Activity, Zap, Filter, Percent } from 'lucide-react';
import { Progress } from "@/components/ui/progress";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from "@/components/ui/tooltip";

interface EfficiencyMetricsProps {
  massEfficiency: number;
  processEfficiency: number;
  separationEfficiency: number;
  proteinYield: number;
}

export function EfficiencyMetrics({
  massEfficiency,
  processEfficiency,
  separationEfficiency,
  proteinYield,
}: EfficiencyMetricsProps) {
  const metrics = [
    {
      title: 'Mass Efficiency',
      value: massEfficiency,
      icon: <Activity className="h-4 w-4" />,
      suffix: '%',
      tooltip: 'Ratio of recovered mass to input mass',
      threshold: 85,
    },
    {
      title: 'Process Efficiency',
      value: processEfficiency,
      icon: <Zap className="h-4 w-4" />,
      suffix: '%',
      tooltip: 'Overall process performance efficiency',
      threshold: 90,
    },
    {
      title: 'Separation Efficiency',
      value: separationEfficiency,
      icon: <Filter className="h-4 w-4" />,
      suffix: '%',
      tooltip: 'Efficiency of protein separation process',
      threshold: 80,
    },
    {
      title: 'Protein Yield',
      value: proteinYield,
      icon: <Percent className="h-4 w-4" />,
      suffix: '%',
      tooltip: 'Total protein yield from the process',
      threshold: 95,
    },
  ];

  return (
    <Card>
      <CardHeader>
        <CardTitle>Process Efficiency Metrics</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="grid gap-4 sm:grid-cols-2">
          {metrics.map((metric, index) => (
            <TooltipProvider key={index}>
              <Tooltip>
                <TooltipTrigger asChild>
                  <Card>
                    <CardContent className="pt-6">
                      <div className="flex items-center gap-2">
                        <div
                          className={`rounded-full p-2 ${
                            metric.value >= metric.threshold
                              ? 'bg-emerald-100 text-emerald-700'
                              : 'bg-blue-100 text-blue-700'
                          }`}
                        >
                          {metric.icon}
                        </div>
                        <div className="flex-1">
                          <p className="text-sm font-medium text-muted-foreground">
                            {metric.title}
                          </p>
                          <p
                            className={`text-2xl font-bold ${
                              metric.value >= metric.threshold
                                ? 'text-emerald-600'
                                : 'text-blue-600'
                            }`}
                          >
                            {metric.value.toFixed(1)}{metric.suffix}
                          </p>
                        </div>
                      </div>
                      <div className="mt-4">
                        <Progress
                          value={Math.min(100, Math.max(0, metric.value))}
                          className={metric.value >= metric.threshold ? 'bg-emerald-100' : 'bg-blue-100'}
                          indicatorColor={
                            metric.value >= metric.threshold
                              ? 'rgb(16 185 129)'  // emerald-500
                              : 'rgb(59 130 246)'  // blue-500
                          }
                        />
                      </div>
                    </CardContent>
                  </Card>
                </TooltipTrigger>
                <TooltipContent>
                  <p>{metric.tooltip}</p>
                </TooltipContent>
              </Tooltip>
            </TooltipProvider>
          ))}
        </div>
      </CardContent>
    </Card>
  );
} 