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

  const processContributionData = Object.entries(process_contributions).map(([category, contributions]) => ({
    category,
    ...Object.entries(contributions as Record<string, ProcessContribution>).reduce((acc, [process, data]) => ({
      ...acc,
      [process]: data.value / impactResults.metadata.total_mass,
      [`${process}_unit`]: `${data.unit}/kg`,
    }), {} as Record<string, string | number>),
  })) as ProcessContributionData[];

  const processData = [
    {
      name: 'Air Classifier Milling',
      contribution: impactResults.process_breakdown.air_classifier_milling * 100
    },
    {
      name: 'Air Classification',
      contribution: impactResults.process_breakdown.air_classification * 100
    },
    {
      name: 'RF Treatment',
      contribution: impactResults.process_breakdown.rf_treatment * 100
    },
    {
      name: 'Tempering',
      contribution: impactResults.process_breakdown.tempering * 100
    },
    {
      name: 'Hammer Milling',
      contribution: impactResults.process_breakdown.hammer_milling * 100
    },
    {
      name: 'Dehulling',
      contribution: impactResults.process_breakdown.dehulling * 100
    }
  ];

  const sourceData = [
    {
      category: 'Electricity',
      gwp: process_contributions.gwp.electricity.value,
      water: process_contributions.water.cooling.value,
      resource: process_contributions.frs.electricity.value,
      unit: {
        gwp: 'kg CO₂e',
        water: 'kg',
        resource: 'kg oil eq'
      }
    },
    {
      category: 'Process Water',
      gwp: process_contributions.gwp.water.value,
      water: process_contributions.water.tempering.value + 
            process_contributions.water.cleaning.value,
      resource: 0, // Water use doesn't directly contribute to resource scarcity
      unit: {
        gwp: 'kg CO₂e',
        water: 'kg',
        resource: 'kg oil eq'
      }
    },
    {
      category: 'Transport & Equipment',
      gwp: process_contributions.gwp.transport.value,
      water: 0, // Transport doesn't directly use water
      resource: process_contributions.frs.mechanical_processing.value,
      unit: {
        gwp: 'kg CO₂e',
        water: 'kg',
        resource: 'kg oil eq'
      }
    }
  ];

  // Add process efficiency metrics
  const processEfficiency = {
    energy: {
      value: impactResults.metadata.energy_intensity,
      benchmark: 0.65,
      unit: 'kWh/kg'
    },
    water: {
      value: impactResults.metadata.water_intensity,
      benchmark: 0.55,
      unit: 'kg/kg'
    },
    thermal: {
      value: impactResults.metadata.thermal_ratio,
      benchmark: 0.65,
      unit: ''
    }
  };

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <div className="flex items-center gap-2">
            <CardTitle>Process Contribution Analysis</CardTitle>
            <Tooltip>
              <TooltipTrigger>
                <HelpCircle className="h-4 w-4 text-muted-foreground" />
              </TooltipTrigger>
              <TooltipContent>
                <p className="max-w-xs">
                  Breakdown of environmental impacts by process step and resource type.
                  Values are normalized per kg of final product.
                </p>
              </TooltipContent>
            </Tooltip>
          </div>
        </CardHeader>
        <CardContent>
          <div className="space-y-6">
            {/* Process Contribution Chart */}
            <div>
              <h3 className="text-sm font-medium mb-2">Process Energy Consumption Breakdown</h3>
              <div className="flex items-center gap-2 mb-2">
                <span className="text-sm text-muted-foreground">
                  Distribution of energy consumption across process steps
                </span>
                <Tooltip>
                  <TooltipTrigger>
                    <HelpCircle className="h-4 w-4 text-muted-foreground" />
                  </TooltipTrigger>
                  <TooltipContent>
                    <p className="max-w-xs">
                      Percentage of total energy consumption for each process step in the pea protein extraction process
                    </p>
                  </TooltipContent>
                </Tooltip>
              </div>
              <div className="h-[300px]">
                <ResponsiveContainer>
                  <BarChart data={processData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="name" />
                    <YAxis label={{ value: 'Consumption (%)', angle: -90, position: 'insideLeft' }} />
                    <RechartsTooltip />
                    <Bar dataKey="contribution" fill="#10b981" name="Energy Contribution" />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>

            {/* Impact Sources Chart */}
            <div>
              <div className="flex items-center justify-between mb-2">
                <h3 className="text-sm font-medium">Environmental Impact Sources</h3>
                <Tooltip>
                  <TooltipTrigger>
                    <HelpCircle className="h-4 w-4 text-muted-foreground" />
                  </TooltipTrigger>
                  <TooltipContent>
                    <p className="max-w-xs">
                      Distribution of environmental impacts across different process sources
                    </p>
                  </TooltipContent>
                </Tooltip>
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                {/* GWP Chart */}
                <div className="h-[300px]">
                  <h4 className="text-sm font-medium mb-2">Global Warming Potential</h4>
                  <ResponsiveContainer>
                    <BarChart data={sourceData}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="category" />
                      <YAxis label={{ value: 'kg CO₂e', angle: -90, position: 'insideLeft' }} />
                      <RechartsTooltip />
                      <Bar dataKey="gwp" name="GWP" fill="#10b981" />
                    </BarChart>
                  </ResponsiveContainer>
                </div>

                {/* Water Chart */}
                <div className="h-[300px]">
                  <h4 className="text-sm font-medium mb-2">Water Consumption</h4>
                  <ResponsiveContainer>
                    <BarChart data={sourceData}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="category" />
                      <YAxis label={{ value: 'kg water', angle: -90, position: 'insideLeft' }} />
                      <RechartsTooltip />
                      <Bar dataKey="water" name="Water" fill="#0ea5e9" />
                    </BarChart>
                  </ResponsiveContainer>
                </div>

                {/* Resource Use Chart */}
                <div className="h-[300px]">
                  <h4 className="text-sm font-medium mb-2">Resource Use</h4>
                  <ResponsiveContainer>
                    <BarChart data={sourceData}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="category" />
                      <YAxis label={{ value: 'kg oil eq', angle: -90, position: 'insideLeft' }} />
                      <RechartsTooltip />
                      <Bar dataKey="resource" name="Resource" fill="#6366f1" />
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </div>
              
              {/* Add summary table */}
              <div className="mt-4">
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Source</TableHead>
                      <TableHead>GWP (kg CO₂e)</TableHead>
                      <TableHead>Water (kg)</TableHead>
                      <TableHead>Resource Use (kg oil eq)</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {sourceData.map((source) => (
                      <TableRow key={source.category}>
                        <TableCell>{source.category}</TableCell>
                        <TableCell>{source.gwp.toFixed(1)}</TableCell>
                        <TableCell>{source.water.toFixed(1)}</TableCell>
                        <TableCell>{source.resource.toFixed(1)}</TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </div>
            </div>

            {/* Add Process Efficiency Table */}
            <div>
              <h3 className="text-sm font-medium mb-2">Process Efficiency Metrics</h3>
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Metric</TableHead>
                    <TableHead>Current</TableHead>
                    <TableHead>Benchmark</TableHead>
                    <TableHead>Status</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  <TableRow>
                    <TableCell>Energy Intensity</TableCell>
                    <TableCell>{processEfficiency.energy.value.toFixed(2)} {processEfficiency.energy.unit}</TableCell>
                    <TableCell>{processEfficiency.energy.benchmark} {processEfficiency.energy.unit}</TableCell>
                    <TableCell>
                      <span className={processEfficiency.energy.value <= processEfficiency.energy.benchmark ? 
                        "text-green-600" : "text-amber-600"}>
                        {processEfficiency.energy.value <= processEfficiency.energy.benchmark ? "Optimal" : "Above Target"}
                      </span>
                    </TableCell>
                  </TableRow>
                  <TableRow>
                    <TableCell>Water Intensity</TableCell>
                    <TableCell>{processEfficiency.water.value.toFixed(2)} {processEfficiency.water.unit}</TableCell>
                    <TableCell>{processEfficiency.water.benchmark} {processEfficiency.water.unit}</TableCell>
                    <TableCell>
                      <span className={processEfficiency.water.value <= processEfficiency.water.benchmark ? 
                        "text-green-600" : "text-amber-600"}>
                        {processEfficiency.water.value <= processEfficiency.water.benchmark ? "Optimal" : "Above Target"}
                      </span>
                    </TableCell>
                  </TableRow>
                  <TableRow>
                    <TableCell>Thermal Efficiency</TableCell>
                    <TableCell>{(processEfficiency.thermal.value * 100).toFixed(1)}%</TableCell>
                    <TableCell>{(processEfficiency.thermal.benchmark * 100).toFixed(1)}%</TableCell>
                    <TableCell>
                      <span className={processEfficiency.thermal.value >= processEfficiency.thermal.benchmark ? 
                        "text-green-600" : "text-amber-600"}>
                        {processEfficiency.thermal.value >= processEfficiency.thermal.benchmark ? "Optimal" : "Below Target"}
                      </span>
                    </TableCell>
                  </TableRow>
                </TableBody>
              </Table>
            </div>

            {/* RF Treatment Details */}
            <div>
              <h3 className="text-sm font-medium mb-2">RF Treatment Performance</h3>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="p-4 bg-muted rounded-lg">
                  <div className="flex items-center justify-between">
                    <span className="text-sm font-medium">Energy Contribution</span>
                    <Tooltip>
                      <TooltipTrigger>
                        <HelpCircle className="h-4 w-4 text-muted-foreground" />
                      </TooltipTrigger>
                      <TooltipContent>
                        <p className="max-w-xs">
                          Current RF energy contribution is {(impactResults.rf_parameters.contribution_percentage).toFixed(1)}% 
                          of total process energy. The optimal contribution should be 19±1% based on research. 
                          Current value indicates RF treatment may be underpowered relative to other process steps.
                        </p>
                      </TooltipContent>
                    </Tooltip>
                  </div>
                  <p className="text-2xl font-semibold mt-2">
                    {(impactResults.rf_parameters.contribution_percentage).toFixed(1)}%
                  </p>
                  <div className="flex items-center justify-between mt-1">
                    <p className="text-sm text-muted-foreground">
                      Current
                    </p>
                    <p className="text-sm font-medium">
                      Target: 19±1%
                    </p>
                  </div>
                  <div className={`text-sm mt-2 ${
                    impactResults.rf_parameters.contribution_percentage >= 18 && 
                    impactResults.rf_parameters.contribution_percentage <= 20 
                      ? "text-green-600" 
                      : "text-amber-600"
                  }`}>
                    {impactResults.rf_parameters.contribution_percentage >= 18 && 
                     impactResults.rf_parameters.contribution_percentage <= 20 
                      ? "Within optimal range" 
                      : "Below optimal range - RF treatment may need more power"
                    }
                  </div>
                </div>
                <div className="p-4 bg-muted rounded-lg">
                  <div className="flex items-center justify-between">
                    <span className="text-sm font-medium">Temperature Control</span>
                    <Tooltip>
                      <TooltipTrigger>
                        <HelpCircle className="h-4 w-4 text-muted-foreground" />
                      </TooltipTrigger>
                      <TooltipContent>
                        <p className="max-w-xs">
                          Outfeed temperature (temperature at which seeds exit the conveyer belt) should be 84.4±5°C for optimal protein extraction. Electrode temperature: {impactResults.rf_parameters.temperature_electrode}°C
                        </p>
                      </TooltipContent>
                    </Tooltip>
                  </div>
                  <p className="text-2xl font-semibold mt-2">
                    {impactResults.rf_parameters.temperature_outfeed}°C
                  </p>
                  <p className="text-sm text-muted-foreground mt-1">
                    Target: 84.4±5°C
                  </p>
                  <div className={`text-sm mt-2 ${Math.abs(impactResults.rf_parameters.temperature_outfeed - 84.4) <= 5 ? "text-green-600" : "text-amber-600"}`}>
                    {Math.abs(impactResults.rf_parameters.temperature_outfeed - 84.4) <= 5 ? "Within optimal range" : "Outside optimal range"}
                  </div>
                </div>
                <div className="p-4 bg-muted rounded-lg">
                  <div className="flex items-center justify-between">
                    <span className="text-sm font-medium">Energy Consumption</span>
                    <Tooltip>
                      <TooltipTrigger>
                        <HelpCircle className="h-4 w-4 text-muted-foreground" />
                      </TooltipTrigger>
                      <TooltipContent>
                        <p className="max-w-xs">
                          RF energy consumption per batch at frequency 27.12 MHz, conveyor speed 0.17 m/min, material depth 30 mm, electrode gap 86.9 mm
                        </p>
                      </TooltipContent>
                    </Tooltip>
                  </div>
                  <p className="text-2xl font-semibold mt-2">
                    {impactResults.rf_parameters.energy_consumption} kWh
                  </p>
                  <p className="text-sm text-muted-foreground mt-1">
                    Operating Parameters:
                  </p>
                  <div className="text-xs text-muted-foreground mt-1">
                    Anode: {impactResults.rf_parameters.anode_current}A, Grid: {impactResults.rf_parameters.grid_current}A
                  </div>
                </div>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
} 