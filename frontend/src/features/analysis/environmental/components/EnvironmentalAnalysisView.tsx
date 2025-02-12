"use client";

import React from 'react';
import { EnvironmentalResults } from '@/types/environmental';
import { formatNumber } from '@/lib/formatters';
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { Separator } from "@/components/ui/separator";
import { EmissionsBreakdown } from './EmissionsBreakdown';
import { ResourceConsumption } from './ResourceConsumption';
import { ImpactMetrics } from './ImpactMetrics';

interface EnvironmentalAnalysisViewProps {
  data: EnvironmentalResults;
}

export function EnvironmentalAnalysisView({ data }: EnvironmentalAnalysisViewProps) {
  const metrics = [
    {
      title: 'Carbon Footprint',
      value: data.carbonFootprint,
      unit: 'kg CO₂e',
      color: 'rgb(59 130 246)', // blue-500
      bgColor: 'bg-blue-100',
    },
    {
      title: 'Water Footprint',
      value: data.waterFootprint,
      unit: 'm³',
      color: 'rgb(34 211 238)', // cyan-500
      bgColor: 'bg-cyan-100',
    },
    {
      title: 'Energy Efficiency',
      value: data.energyEfficiency,
      unit: '%',
      color: 'rgb(34 197 94)', // green-500
      bgColor: 'bg-green-100',
    }
  ];

  return (
    <div className="space-y-6">
      {/* Key Metrics */}
      <div className="grid gap-4 md:grid-cols-3">
        {metrics.map((metric) => (
          <Card key={metric.title}>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">
                {metric.title}
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-2">
                <div className="flex items-center justify-between">
                  <span className="text-2xl font-bold">
                    {formatNumber(metric.value)}
                    <span className="ml-1 text-sm font-normal text-muted-foreground">
                      {metric.unit}
                    </span>
                  </span>
                </div>
                <Progress
                  value={metric.title === 'Energy Efficiency' ? metric.value : (metric.value / 100) * 75}
                  className={metric.bgColor}
                  indicatorColor={metric.color}
                />
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      <Separator />

      {/* Emissions and Resource Components */}
      <div className="grid gap-6 md:grid-cols-2">
        <EmissionsBreakdown
          impactAssessment={{
            gwp: data.carbonFootprint,
            hct: data.toxicityScore || 0,
            frs: data.resourceDepletion || 0,
          }}
          processType={data.processType}
        />
        <ResourceConsumption
          consumptionMetrics={{
            electricity: data.resourceConsumption.electricity,
            cooling: data.resourceConsumption.cooling || null,
            water: data.resourceConsumption.water,
          }}
          processType={data.processType}
        />
      </div>

      <Separator />

      {/* Impact Metrics */}
      <ImpactMetrics
        impacts={{
          gwp: data.carbonFootprint,
          hct: data.toxicityScore || 0,
          frs: data.resourceDepletion || 0,
        }}
        allocatedImpacts={{
          method: data.allocationMethod || 'mass',
          factors: data.allocationFactors || {},
          results: data.allocatedImpacts || {},
        }}
      />

      {/* Waste Management */}
      <Card>
        <CardHeader>
          <CardTitle>Waste Management</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex flex-col items-center space-y-4">
            <div className="text-center">
              <h4 className="text-sm font-medium text-muted-foreground mb-4">
                Waste Recycling Rate
              </h4>
              <div className="relative h-40 w-40">
                <div className="absolute inset-0 flex items-center justify-center">
                  <span className="text-3xl font-bold">
                    {formatNumber(data.wasteRecyclingRate * 100)}%
                  </span>
                </div>
                <svg
                  className="h-full w-full"
                  viewBox="0 0 100 100"
                >
                  <circle
                    className="stroke-muted fill-none"
                    cx="50"
                    cy="50"
                    r="45"
                    strokeWidth="10"
                  />
                  <circle
                    className="stroke-primary fill-none"
                    cx="50"
                    cy="50"
                    r="45"
                    strokeWidth="10"
                    strokeDasharray={`${data.wasteRecyclingRate * 283} 283`}
                    transform="rotate(-90 50 50)"
                  />
                </svg>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
} 