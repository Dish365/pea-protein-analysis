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
  Tooltip as RechartsTooltip,
  Legend,
  ResponsiveContainer,
  TooltipProps,
} from 'recharts';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { HelpCircle } from "lucide-react";
import { Tooltip, TooltipContent, TooltipTrigger } from "@/components/ui/tooltip";

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

// Replace the existing ImpactKey type with:
type ImpactKey = 'gwp' | 'hct' | 'frs' | 'water_consumption';

export function ImpactMetrics({
  impactResults,
  allocationResults,
}: ImpactMetricsProps) {
  const { total_impacts, process_contributions } = impactResults;

  // Format total impacts data
  const totalImpactData = [
    {
      name: 'Global Warming',
      value: total_impacts.gwp / impactResults.metadata.total_mass,
      unit: 'kg CO₂e/kg',
      description: 'Global Warming Potential per kg product',
    },
    {
      name: 'Human Toxicity',
      value: total_impacts.hct / impactResults.metadata.total_mass,
      unit: 'CTUh/kg',
      description: 'Human Toxicity Potential per kg product',
    },
    {
      name: 'Resource Scarcity',
      value: total_impacts.frs / impactResults.metadata.total_mass,
      unit: 'kg oil eq/kg',
      description: 'Fossil Resource Scarcity per kg product',
    },
    {
      name: 'Water Consumption',
      value: total_impacts.water_consumption / impactResults.metadata.total_mass,
      unit: 'kg/kg',
      description: 'Water Consumption per kg product',
    },
  ];

  // Format allocation data
  const allocationData = [
    {
      name: 'Protein Concentrate',
      gwp: allocationResults.allocated_impacts.gwp.protein_concentrate / impactResults.metadata.mass_flows.protein_concentrate,
      hct: allocationResults.allocated_impacts.hct.protein_concentrate / impactResults.metadata.mass_flows.protein_concentrate,
      frs: allocationResults.allocated_impacts.frs.protein_concentrate / impactResults.metadata.mass_flows.protein_concentrate,
      water: allocationResults.allocated_impacts.water_consumption.protein_concentrate / impactResults.metadata.mass_flows.protein_concentrate,
    },
    {
      name: 'Starch',
      gwp: allocationResults.allocated_impacts.gwp.starch / impactResults.metadata.mass_flows.starch,
      hct: allocationResults.allocated_impacts.hct.starch / impactResults.metadata.mass_flows.starch,
      frs: allocationResults.allocated_impacts.frs.starch / impactResults.metadata.mass_flows.starch,
      water: allocationResults.allocated_impacts.water_consumption.starch / impactResults.metadata.mass_flows.starch,
    },
    {
      name: 'Fiber',
      gwp: allocationResults.allocated_impacts.gwp.fiber / impactResults.metadata.mass_flows.fiber,
      hct: allocationResults.allocated_impacts.hct.fiber / impactResults.metadata.mass_flows.fiber,
      frs: allocationResults.allocated_impacts.frs.fiber / impactResults.metadata.mass_flows.fiber,
      water: allocationResults.allocated_impacts.water_consumption.fiber / impactResults.metadata.mass_flows.fiber,
    }
  ];

  // Update the impact benchmarks section
  const impactBenchmarks = {
    gwp: { 
      key: 'gwp',
      label: 'Global Warming',
      value: 0.45, 
      unit: 'kg CO₂e/kg',
      description: 'Carbon dioxide equivalent emissions per kg product'
    },
    water_consumption: { 
      key: 'water_consumption',
      label: 'Water',
      value: 4.5, 
      unit: 'kg/kg',
      description: 'Process water consumption per kg product'
    },
    frs: { 
      key: 'frs',
      label: 'Resource Scarcity',
      value: 0.25, 
      unit: 'kg oil eq/kg',
      description: 'Fossil resource scarcity per kg product'
    },
    hct: { 
      key: 'hct',
      label: 'Human Toxicity',
      value: 2.5e-5, 
      unit: 'CTUh/kg',
      description: 'Comparative toxic units for human health per kg product'
    }
  };

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <CardTitle>Product Impact Allocation</CardTitle>
              <Tooltip>
                <TooltipTrigger>
                  <HelpCircle className="h-4 w-4 text-muted-foreground" />
                </TooltipTrigger>
                <TooltipContent>
                  <p className="max-w-xs">
                    Environmental impacts allocated to each product stream using {allocationResults.method_used} allocation.
                    All values are normalized per kg of product.
                  </p>
                </TooltipContent>
              </Tooltip>
            </div>
            <div className="text-sm text-muted-foreground">
              Method: {allocationResults.method_used}
            </div>
          </div>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* GWP Chart */}
            <div className="h-[300px]">
              <h3 className="text-sm font-medium mb-2">Global Warming Potential</h3>
              <ResponsiveContainer>
                <BarChart data={allocationData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" />
                  <YAxis label={{ value: 'kg CO₂e/kg product', angle: -90, position: 'insideLeft' }} />
                  <RechartsTooltip />
                  <Bar dataKey="gwp" fill="#10b981" name="GWP" />
                </BarChart>
              </ResponsiveContainer>
            </div>

            {/* Water Consumption Chart */}
            <div className="h-[300px]">
              <h3 className="text-sm font-medium mb-2">Water Consumption</h3>
              <ResponsiveContainer>
                <BarChart data={allocationData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" />
                  <YAxis label={{ value: 'kg water/kg product', angle: -90, position: 'insideLeft' }} />
                  <RechartsTooltip />
                  <Bar dataKey="water" fill="#0ea5e9" name="Water" />
                </BarChart>
              </ResponsiveContainer>
            </div>

            {/* Resource Scarcity Chart */}
            <div className="h-[300px]">
              <h3 className="text-sm font-medium mb-2">Resource Scarcity</h3>
              <ResponsiveContainer>
                <BarChart data={allocationData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" />
                  <YAxis label={{ value: 'kg oil eq/kg product', angle: -90, position: 'insideLeft' }} />
                  <RechartsTooltip />
                  <Bar dataKey="frs" fill="#6366f1" name="FRS" />
                </BarChart>
              </ResponsiveContainer>
            </div>

            {/* Human Toxicity Chart */}
            <div className="h-[300px]">
              <h3 className="text-sm font-medium mb-2">Human Toxicity</h3>
              <ResponsiveContainer>
                <BarChart data={allocationData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" />
                  <YAxis label={{ value: 'CTUh/kg product', angle: -90, position: 'insideLeft' }} />
                  <RechartsTooltip />
                  <Bar dataKey="hct" fill="#3b82f6" name="HCT" />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* Add Allocation Factors Table */}
          <div className="mt-6">
            <h3 className="text-sm font-medium mb-2">Allocation Factors</h3>
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Product</TableHead>
                  <TableHead>Mass Flow (kg)</TableHead>
                  <TableHead>Allocation Factor</TableHead>
                  <TableHead>Impact Share</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {Object.entries(allocationResults.allocation_factors).map(([product, factor]) => (
                  <TableRow key={product}>
                    <TableCell className="font-medium capitalize">
                      {product.replace(/_/g, ' ')}
                    </TableCell>
                    <TableCell>
                      {impactResults.metadata.mass_flows[product]}
                    </TableCell>
                    <TableCell>
                      {(factor * 100).toFixed(1)}%
                    </TableCell>
                    <TableCell>
                      <div className="flex items-center gap-2">
                        <div className="w-24 h-2 rounded-full bg-gray-200">
                          <div 
                            className="h-full rounded-full bg-primary"
                            style={{ width: `${factor * 100}%` }}
                          />
                        </div>
                        <span className="text-sm text-muted-foreground">
                          {(factor * 100).toFixed(1)}%
                        </span>
                      </div>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </div>

          {/* Add Impact Benchmarks */}
          <div className="mt-6">
            <h3 className="text-sm font-medium mb-2">Impact Benchmarks</h3>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              {Object.values(impactBenchmarks).map((benchmark) => {
                const currentValue = total_impacts[benchmark.key as ImpactKey] / impactResults.metadata.total_mass;
                const isWithinBenchmark = currentValue <= benchmark.value;
                const formattedValue = benchmark.key === 'hct' 
                  ? currentValue.toExponential(2) 
                  : currentValue.toFixed(2);
                
                return (
                  <div key={benchmark.key} className="p-4 bg-muted rounded-lg">
                    <div className="flex items-center justify-between">
                      <span className="text-sm font-medium">{benchmark.label}</span>
                      <Tooltip>
                        <TooltipTrigger>
                          <HelpCircle className="h-4 w-4 text-muted-foreground" />
                        </TooltipTrigger>
                        <TooltipContent>
                          <p className="max-w-xs">{benchmark.description}</p>
                          <p className="text-sm mt-1">Benchmark: {benchmark.value} {benchmark.unit}</p>
                        </TooltipContent>
                      </Tooltip>
                    </div>
                    <p className="text-2xl font-semibold mt-2">
                      {formattedValue} {benchmark.unit}
                    </p>
                    <p className={`text-sm mt-1 ${isWithinBenchmark ? 'text-green-600' : 'text-amber-600'}`}>
                      {isWithinBenchmark ? 'Within Benchmark' : 'Above Benchmark'}
                    </p>
                  </div>
                );
              })}
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
} 