"use client";

import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { ImpactAssessment } from '@/types/environmental';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';

interface ImpactMetricsProps {
  impacts: ImpactAssessment;
  allocatedImpacts: {
    method: string;
    factors: Record<string, number>;
    results: Record<string, ImpactAssessment>;
  };
}

export function ImpactMetrics({
  impacts,
  allocatedImpacts,
}: ImpactMetricsProps) {
  const impactData = [
    {
      name: 'Global Warming',
      value: impacts.gwp,
      unit: 'kg CO₂e',
      description: 'Global Warming Potential',
    },
    {
      name: 'Human Toxicity',
      value: impacts.hct,
      unit: 'CTUh',
      description: 'Human Toxicity Potential',
    },
    {
      name: 'Resource Scarcity',
      value: impacts.frs,
      unit: 'MJ',
      description: 'Fossil Resource Scarcity',
    },
  ];

  const allocationData = Object.entries(allocatedImpacts.results).map(([key, value]) => ({
    name: key,
    gwp: value.gwp,
    hct: value.hct,
    frs: value.frs,
  }));

  return (
    <Card>
      <CardHeader>
        <CardTitle>Impact Assessment</CardTitle>
        <p className="text-sm text-muted-foreground">
          Allocation Method: {allocatedImpacts.method}
        </p>
      </CardHeader>
      <CardContent>
        <div className="space-y-6">
          <div className="h-[300px]">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={impactData} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip
                  content={({ active, payload }) => {
                    if (active && payload && payload.length) {
                      const data = payload[0].payload;
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

          <div className="h-[300px]">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={allocationData} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Bar dataKey="gwp" name="GWP" fill="#10b981" stackId="a" />
                <Bar dataKey="hct" name="HCT" fill="#3b82f6" stackId="a" />
                <Bar dataKey="frs" name="FRS" fill="#6366f1" stackId="a" />
              </BarChart>
            </ResponsiveContainer>
          </div>

          <div className="grid grid-cols-3 gap-4">
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