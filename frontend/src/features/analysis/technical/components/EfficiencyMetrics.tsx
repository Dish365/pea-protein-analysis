"use client";

import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";

export interface EfficiencyMetricsProps {
  separationEfficiency: number;
  processEfficiency: number;
  proteinYield: number;
}

export function EfficiencyMetrics({
  separationEfficiency,
  processEfficiency,
  proteinYield,
}: EfficiencyMetricsProps) {
  const metrics = [
    {
      label: "Separation Efficiency",
      value: separationEfficiency,
      description: "Effectiveness of protein separation process",
    },
    {
      label: "Process Efficiency",
      value: processEfficiency,
      description: "Overall process performance and resource utilization",
    },
    {
      label: "Protein Yield",
      value: proteinYield,
      description: "Final protein recovery rate",
    },
  ];

  return (
    <Card>
      <CardHeader>
        <CardTitle>Process Efficiency Metrics</CardTitle>
      </CardHeader>
      <CardContent className="space-y-6">
        {metrics.map((metric) => (
          <div key={metric.label} className="space-y-2">
            <div className="flex items-center justify-between">
              <div>
                <p className="font-medium">{metric.label}</p>
                <p className="text-sm text-muted-foreground">
                  {metric.description}
                </p>
              </div>
              <span className="text-lg font-semibold">
                {metric.value.toFixed(1)}%
              </span>
            </div>
            <Progress value={metric.value} className="h-2" />
          </div>
        ))}
      </CardContent>
    </Card>
  );
} 