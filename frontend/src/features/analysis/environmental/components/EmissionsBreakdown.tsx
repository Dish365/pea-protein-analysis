"use client";

import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { ImpactResults, AllocationResults } from '@/types/environmental';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  TooltipProps,
} from 'recharts';

interface EmissionsBreakdownProps {
  impactResults: ImpactResults;
  allocationResults: AllocationResults;
}

interface ProcessContribution {
  value: number;
  unit: string;
  process: string;
}

interface ProcessContributionData {
  category: string;
  [key: string]: string | number;
}

interface ChartTooltipData {
  name: string;
  value: number;
  unit: string;
  description: string;
}

interface ChartEntry {
  name: string;
  value: number;
  dataKey: string;
}

export function EmissionsBreakdown({
  impactResults,
  allocationResults,
}: EmissionsBreakdownProps) {
  const { total_impacts, process_contributions } = impactResults;

  const impactData = [
    {
      name: 'Global Warming',
      value: total_impacts.gwp,
      unit: 'kg CO₂e',
      description: 'Global Warming Potential',
    },
    {
      name: 'Human Toxicity',
      value: total_impacts.hct,
      unit: 'CTUh',
      description: 'Human Toxicity Potential',
    },
    {
      name: 'Resource Scarcity',
      value: total_impacts.frs,
      unit: 'kg oil eq',
      description: 'Fossil Resource Scarcity',
    },
    {
      name: 'Water Consumption',
      value: total_impacts.water_consumption,
      unit: 'kg',
      description: 'Total Water Consumption',
    },
  ];

  const processContributionData = Object.entries(process_contributions).map(([category, contributions]) => ({
    category,
    ...Object.entries(contributions as Record<string, ProcessContribution>).reduce((acc, [process, data]) => ({
      ...acc,
      [process]: data.value,
      [`${process}_unit`]: data.unit,
    }), {} as Record<string, string | number>),
  })) as ProcessContributionData[];

  return (
    <Card>
      <CardHeader>
        <CardTitle>Environmental Impact Breakdown</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-6">
          {/* Total Impacts Chart */}
          <div className="h-[300px]">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={impactData} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip
                  content={({ active, payload }) => {
                    if (active && payload && payload.length) {
                      const data = payload[0].payload as ChartTooltipData;
                      return (
                        <div className="rounded-lg bg-white p-2 shadow-md border">
                          <p className="font-medium">{data.name}</p>
                          <p className="text-sm text-muted-foreground">
                            {data.description}
                          </p>
                          <p className="mt-1 font-medium">
                            {data.value.toFixed(2)} {data.unit}
                          </p>
                        </div>
                      );
                    }
                    return null;
                  }}
                />
                <Bar
                  dataKey="value"
                  fill="#10b981"
                  radius={[4, 4, 0, 0]}
                />
              </BarChart>
            </ResponsiveContainer>
          </div>

          {/* Process Contributions Chart */}
          <div className="h-[300px]">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={processContributionData} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="category" />
                <YAxis />
                <Tooltip
                  content={({ active, payload, label }: TooltipProps<number, string>) => {
                    if (active && payload && payload.length) {
                      return (
                        <div className="rounded-lg bg-white p-2 shadow-md border">
                          <p className="font-medium">{String(label).toUpperCase()}</p>
                          {payload.map((entry) => {
                            const unitKey = `${entry.dataKey}_unit`;
                            const unit = processContributionData[0][unitKey] as string;
                            return (
                              <p key={entry.dataKey} className="text-sm">
                                {String(entry.name)}: {entry.value?.toFixed(2)} {unit}
                              </p>
                            );
                          })}
                        </div>
                      );
                    }
                    return null;
                  }}
                />
                <Legend />
                {Object.keys(process_contributions.gwp).map((process, index) => (
                  <Bar
                    key={process}
                    dataKey={process}
                    name={process}
                    fill={`hsl(${index * 60}, 70%, 50%)`}
                    radius={[4, 4, 0, 0]}
                  />
                ))}
              </BarChart>
            </ResponsiveContainer>
          </div>

          {/* Summary Grid */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {impactData.map((impact) => (
              <div key={impact.name} className="text-center">
                <p className="text-sm font-medium text-muted-foreground">{impact.name}</p>
                <p className="text-lg font-semibold">
                  {impact.value.toFixed(2)} {impact.unit}
                </p>
              </div>
            ))}
          </div>
        </div>
      </CardContent>
    </Card>
  );
} 