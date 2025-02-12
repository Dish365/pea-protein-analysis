"use client";

import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { Zap, Recycle, Leaf } from 'lucide-react';

interface SustainabilityScoreProps {
  energyEfficiency: number;
  resourceDepletion: number;
  wasteRecycling: number;
}

export function SustainabilityScore({
  energyEfficiency,
  resourceDepletion,
  wasteRecycling,
}: SustainabilityScoreProps) {
  const metrics = [
    {
      label: "Energy Efficiency",
      value: energyEfficiency,
      icon: <Zap className="h-4 w-4" />,
      description: "Process energy utilization efficiency",
      target: 80,
    },
    {
      label: "Resource Conservation",
      value: 100 - resourceDepletion,
      icon: <Leaf className="h-4 w-4" />,
      description: "Resource conservation rate",
      target: 70,
    },
    {
      label: "Waste Recycling",
      value: wasteRecycling,
      icon: <Recycle className="h-4 w-4" />,
      description: "Waste recycling and recovery rate",
      target: 75,
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
                className="h-2"
              />
            </div>
          );
        })}
      </CardContent>
    </Card>
  );
} 