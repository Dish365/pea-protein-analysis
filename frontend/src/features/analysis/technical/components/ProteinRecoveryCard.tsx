"use client";

import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { ProteinRecovery } from '@/types/technical';

export interface ProteinRecoveryCardProps {
  recovery: ProteinRecovery;
}

export function ProteinRecoveryCard({ recovery }: ProteinRecoveryCardProps) {
  const metrics = [
    {
      label: "Mass Recovery",
      value: recovery.mass,
      description: "Total mass recovered from process",
    },
    {
      label: "Content Recovery",
      value: recovery.content,
      description: "Protein content in recovered material",
    },
    {
      label: "Yield Recovery",
      value: recovery.yield,
      description: "Overall protein yield efficiency",
    },
  ];

  return (
    <Card>
      <CardHeader>
        <CardTitle>Protein Recovery Analysis</CardTitle>
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