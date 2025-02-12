"use client";

import React from 'react';
import { formatNumber } from '@/lib/formatters';
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
import { Badge } from "@/components/ui/badge";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip as RechartsTooltip,
} from 'recharts';

interface ImpactMetricsProps {
  impacts: {
    gwp: number;
    hct: number;
    frs: number;
  };
  allocatedImpacts: {
    method: string;
    factors: Record<string, number>;
    results: Record<string, {
      gwp: number;
      hct: number;
      frs: number;
    }>;
  };
}

interface AllocationData {
  id: string;
  product: string;
  gwp: number;
  hct: number;
  frs: number;
}

export function ImpactMetrics({ impacts, allocatedImpacts }: ImpactMetricsProps) {
  const impactMetrics = [
    {
      key: 'gwp',
      name: 'Global Warming Potential',
      value: impacts.gwp,
      unit: 'kg CO₂eq',
      description: 'Carbon dioxide equivalent emissions',
      benchmark: 100, // Example benchmark
      color: 'rgb(59 130 246)', // blue-500
    },
    {
      key: 'hct',
      name: 'Human Carcinogenic Toxicity',
      value: impacts.hct,
      unit: 'CTUh',
      description: 'Comparative Toxic Units for human health',
      benchmark: 0.1,
      color: 'rgb(147 51 234)', // purple-500
    },
    {
      key: 'frs',
      name: 'Fossil Resource Scarcity',
      value: impacts.frs,
      unit: 'kg oil eq',
      description: 'Oil equivalent of fossil resources used',
      benchmark: 50,
      color: 'rgb(34 211 238)', // cyan-500
    }
  ];

  // Prepare data for Area chart
  const chartData = impactMetrics.map(metric => ({
    category: metric.name,
    value: (metric.value / metric.benchmark) * 100,
    actual: metric.value,
    benchmark: metric.benchmark,
    unit: metric.unit,
    color: metric.color,
  }));

  // Prepare allocation data for table
  const allocationData: AllocationData[] = Object.entries(allocatedImpacts.results).map(([product, impacts]) => ({
    id: product,
    product,
    gwp: impacts.gwp,
    hct: impacts.hct,
    frs: impacts.frs
  }));

  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
        <CardTitle>Environmental Impact Analysis</CardTitle>
        <Badge variant="outline" className="font-mono">
          {allocatedImpacts.method.toUpperCase()}
        </Badge>
      </CardHeader>
      <CardContent>
        <div className="space-y-6">
          <div>
            <h4 className="text-sm font-medium mb-4">Impact Metrics vs Benchmarks</h4>
            <div className="h-[300px] w-full">
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={chartData} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
                  <CartesianGrid strokeDasharray="3 3" className="stroke-muted" />
                  <XAxis 
                    dataKey="category" 
                    className="text-xs"
                    tick={{ fill: 'currentColor' }}
                  />
                  <YAxis 
                    className="text-xs"
                    tick={{ fill: 'currentColor' }}
                    label={{ 
                      value: '% of Benchmark', 
                      angle: -90, 
                      position: 'insideLeft',
                      className: "fill-current"
                    }}
                  />
                  <RechartsTooltip
                    content={({ active, payload }) => {
                      if (active && payload && payload.length) {
                        const data = payload[0].payload;
                        return (
                          <div className="rounded-lg border bg-background p-2 shadow-md">
                            <p className="text-sm font-medium">{data.category}</p>
                            <p className="text-sm text-muted-foreground">
                              {formatNumber(data.actual)} {data.unit}
                            </p>
                            <p className="text-sm text-muted-foreground">
                              {formatNumber(data.value)}% of benchmark
                            </p>
                          </div>
                        );
                      }
                      return null;
                    }}
                  />
                  {impactMetrics.map((metric) => (
                    <Area
                      key={metric.key}
                      type="monotone"
                      dataKey="value"
                      name={metric.name}
                      stroke={metric.color}
                      fill={metric.color}
                      fillOpacity={0.2}
                    />
                  ))}
                </AreaChart>
              </ResponsiveContainer>
            </div>
          </div>

          <div>
            <h4 className="text-sm font-medium mb-4">Allocated Impacts by Product</h4>
            <div className="rounded-md border">
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Product</TableHead>
                    {impactMetrics.map((metric) => (
                      <TableHead key={metric.key}>
                        <TooltipProvider>
                          <Tooltip>
                            <TooltipTrigger className="text-left font-medium">
                              {metric.name}
                            </TooltipTrigger>
                            <TooltipContent>
                              <p>{metric.description}</p>
                            </TooltipContent>
                          </Tooltip>
                        </TooltipProvider>
                      </TableHead>
                    ))}
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {allocationData.map((row) => (
                    <TableRow key={row.id}>
                      <TableCell className="font-medium">{row.product}</TableCell>
                      {impactMetrics.map((metric) => (
                        <TableCell key={metric.key}>
                          {formatNumber(row[metric.key as keyof Omit<AllocationData, 'id' | 'product'>])} {metric.unit}
                        </TableCell>
                      ))}
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  );
} 