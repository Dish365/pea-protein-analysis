"use client";

import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { Zap, Recycle, Leaf } from 'lucide-react';
import { ImpactResults } from '@/types/environmental';

interface SustainabilityScoreProps {
  impactResults: ImpactResults;
}

export function SustainabilityScore({
  impactResults,
}: SustainabilityScoreProps) {
  const { metadata, rf_parameters, process_breakdown } = impactResults;

  const metrics = [
    {
      label: "Energy Efficiency",
      value: (1 - metadata.energy_intensity) * 100,
      icon: <Zap className="h-4 w-4" />,
      description: "Process energy utilization efficiency",
      target: 80,
    },
    {
      label: "Resource Conservation",
      value: (1 - metadata.water_intensity) * 100,
      icon: <Leaf className="h-4 w-4" />,
      description: "Resource conservation rate",
      target: 70,
    },
    {
      label: "RF Treatment Efficiency",
      value: rf_parameters.contribution_percentage,
      icon: <Recycle className="h-4 w-4" />,
      description: "RF treatment contribution to total process",
      target: 19,
    },
  ];

  const overallScore = metrics.reduce((acc, metric) => 
    acc + (metric.value / metric.target) * 100, 0) / metrics.length;

  const getScoreColor = (score: number) => {
    if (score >= 90) return 'text-emerald-600';
    if (score >= 70) return 'text-blue-600';
    return 'text-yellow-600';
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle>Sustainability Score</CardTitle>
        <div className="flex items-center justify-between">
          <p className="text-sm text-muted-foreground">Overall Performance</p>
          <p className={`text-2xl font-bold ${getScoreColor(overallScore)}`}>
            {overallScore.toFixed(1)}%
          </p>
        </div>
      </CardHeader>
      <CardContent className="space-y-6">
        {metrics.map((metric) => {
          const performance = (metric.value / metric.target) * 100;
          return (
            <div key={metric.label} className="space-y-2">
              <div className="flex items-center gap-2">
                <div className={`rounded-full p-2 ${
                  performance >= 90 ? 'bg-emerald-100 text-emerald-700' :
                  performance >= 70 ? 'bg-blue-100 text-blue-700' :
                  'bg-yellow-100 text-yellow-700'
                }`}>
                  {metric.icon}
                </div>
                <div>
                  <p className="font-medium">{metric.label}</p>
                  <p className="text-sm text-muted-foreground">
                    {metric.description}
                  </p>
                </div>
                <div className="ml-auto text-right">
                  <p className={`text-lg font-semibold ${
                    performance >= 90 ? 'text-emerald-600' :
                    performance >= 70 ? 'text-blue-600' :
                    'text-yellow-600'
                  }`}>
                    {metric.value.toFixed(1)}%
                  </p>
                </div>
              </div>
              <Progress
                value={performance}
                className={`h-2 ${
                  performance >= 90 ? 'bg-emerald-100' :
                  performance >= 70 ? 'bg-blue-100' :
                  'bg-yellow-100'
                }`}
              />
            </div>
          );
        })}

        {/* Process Breakdown */}
        <div className="mt-6">
          <h3 className="font-medium mb-3">Process Breakdown</h3>
          <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
            {Object.entries(process_breakdown).map(([process, value]) => (
              <div key={process} className="text-center p-2 bg-muted rounded-lg">
                <p className="text-sm font-medium capitalize">
                  {process.replace(/_/g, ' ')}
                </p>
                <p className="text-lg font-semibold">
                  {(value * 100).toFixed(1)}%
                </p>
              </div>
            ))}
          </div>
        </div>
      </CardContent>
    </Card>
  );
} 