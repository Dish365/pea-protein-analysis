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

interface ImpactMetricsProps {
  impactResults: ImpactResults;
  allocationResults: AllocationResults;
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
  payload: {
    [key: string]: number;
  };
}

export function ImpactMetrics({
  impactResults,
  allocationResults,
}: ImpactMetricsProps) {
  const { total_impacts, process_contributions } = impactResults;

  // Format total impacts data
  const totalImpactData = [
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

  // Format allocation data
  const allocationData = Object.entries(allocationResults.allocated_impacts.gwp).map(([product, value]) => ({
    product,
    gwp: value,
    hct: allocationResults.allocated_impacts.hct[product],
    frs: allocationResults.allocated_impacts.frs[product],
    water: allocationResults.allocated_impacts.water_consumption[product],
  }));

  return (
    <Card>
      <CardHeader>
        <CardTitle>Impact Assessment</CardTitle>
        <p className="text-sm text-muted-foreground">
          Allocation Method: {allocationResults.method_used}
        </p>
      </CardHeader>
      <CardContent>
        <div className="space-y-6">
          {/* Total Impacts Chart */}
          <div className="h-[300px]">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={totalImpactData} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
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

          {/* Allocated Impacts Chart */}
          <div className="h-[300px]">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={allocationData} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="product" />
                <YAxis />
                <Tooltip
                  content={({ active, payload, label }: TooltipProps<number, string>) => {
                    if (active && payload && payload.length) {
                      return (
                        <div className="rounded-lg bg-white p-2 shadow-md border">
                          <p className="font-medium capitalize">{String(label).replace('_', ' ')}</p>
                          {payload.map((entry) => {
                            if (!entry.dataKey) return null;
                            const value = entry.payload && typeof entry.payload === 'object' 
                              ? (entry.payload as Record<string, number>)[entry.dataKey]
                              : 0;
                            return (
                              <p key={entry.dataKey} className="text-sm">
                                {String(entry.dataKey).toUpperCase()}: {value.toFixed(2)}
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
                <Bar dataKey="gwp" name="GWP" fill="#10b981" stackId="a" />
                <Bar dataKey="hct" name="HCT" fill="#3b82f6" stackId="a" />
                <Bar dataKey="frs" name="FRS" fill="#6366f1" stackId="a" />
                <Bar dataKey="water" name="Water" fill="#0ea5e9" stackId="a" />
              </BarChart>
            </ResponsiveContainer>
          </div>

          {/* Summary Grid */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {totalImpactData.map((impact) => (
              <div key={impact.name} className="text-center">
                <p className="text-sm font-medium text-muted-foreground">{impact.name}</p>
                <p className="text-lg font-semibold">
                  {impact.value.toFixed(2)} {impact.unit}
                </p>
              </div>
            ))}
          </div>

          {/* Allocation Factors */}
          <div className="mt-6">
            <h3 className="font-medium mb-3">Allocation Factors</h3>
            <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
              {Object.entries(allocationResults.allocation_factors).map(([product, factor]) => (
                <div key={product} className="text-center p-2 bg-muted rounded-lg">
                  <p className="text-sm font-medium capitalize">
                    {product.replace(/_/g, ' ')}
                  </p>
                  <p className="text-lg font-semibold">
                    {(factor * 100).toFixed(1)}%
                  </p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  );
} 