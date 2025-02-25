"use client";

import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { ImpactResults } from '@/types/environmental';
import { Zap, Droplets, Snowflake, Factory, HelpCircle } from 'lucide-react';
import { Tooltip, TooltipContent, TooltipTrigger } from "@/components/ui/tooltip";

interface ResourceConsumptionProps {
  impactResults: ImpactResults;
}

export function ResourceConsumption({
  impactResults,
}: ResourceConsumptionProps) {
  const { process_contributions, metadata } = impactResults;

  // Calculate total energy consumption
  const totalElectricity = metadata.energy_intensity * metadata.total_mass;
  const benchmarkEnergyIntensity = 0.65; // kWh/kg from research
  const benchmarkWaterIntensity = 0.55; // kg/kg from research

  const consumptionData = [
    {
      name: 'Electricity',
      value: totalElectricity,
      unit: 'kWh',
      icon: <Zap className="h-4 w-4" />,
      bgColor: 'bg-orange-100',
      textColor: 'text-orange-700',
      description: 'Total electricity consumption for RF treatment process',
      benchmark: benchmarkEnergyIntensity * metadata.total_mass,
      status: metadata.energy_intensity <= benchmarkEnergyIntensity ? 'Within Limit' : 'Exceeding Limit',
      statusColor: metadata.energy_intensity <= benchmarkEnergyIntensity ? 'text-emerald-700 bg-emerald-50' : 'text-red-700 bg-red-50',
      tooltip: `Current energy intensity is ${metadata.energy_intensity.toFixed(2)} kWh/kg. Maximum recommended intensity is ${benchmarkEnergyIntensity} kWh/kg for optimal efficiency.`
    },
    {
      name: 'Process Water',
      value: metadata.water_intensity * metadata.total_mass,
      unit: 'kg',
      icon: <Droplets className="h-4 w-4" />,
      bgColor: 'bg-blue-100',
      textColor: 'text-blue-700',
      description: 'Water used in tempering and cleaning processes',
      benchmark: benchmarkWaterIntensity * metadata.total_mass,
      status: metadata.water_intensity <= benchmarkWaterIntensity ? 'Within Limit' : 'Exceeding Limit',
      statusColor: metadata.water_intensity <= benchmarkWaterIntensity ? 'text-emerald-700 bg-emerald-50' : 'text-red-700 bg-red-50',
      tooltip: `Current water intensity is ${metadata.water_intensity.toFixed(2)} kg/kg. Maximum recommended intensity is ${benchmarkWaterIntensity} kg/kg for optimal resource usage.`
    },
    {
      name: 'Cooling System',
      value: process_contributions.water.cooling.value,
      unit: 'kg/kWh',
      icon: <Snowflake className="h-4 w-4" />,
      bgColor: 'bg-sky-100',
      textColor: 'text-sky-700',
      description: 'Cooling water required per unit of energy',
      isEfficiencyMetric: true,
      benchmark: 300, // Standard cooling water requirement for RF treatment
      status: process_contributions.water.cooling.value <= 300 ? 'Efficient' : 'High Usage',
      statusColor: process_contributions.water.cooling.value <= 300 ? 'text-emerald-700 bg-emerald-50' : 'text-amber-700 bg-amber-50',
      tooltip: `Current cooling efficiency is ${process_contributions.water.cooling.value.toFixed(1)} kg/kWh. Target: ≤300 kg/kWh for optimal cooling efficiency. Lower values indicate better cooling system performance.`
    },
    {
      name: 'Thermal Efficiency',
      value: metadata.thermal_ratio * 100,
      unit: '%',
      icon: <Factory className="h-4 w-4" />,
      bgColor: 'bg-purple-100',
      textColor: 'text-purple-700',
      description: 'Ratio of useful heat to total energy input',
      benchmark: 65,
      status: metadata.thermal_ratio >= 0.65 ? 'Meeting Target' : 'Below Target',
      statusColor: metadata.thermal_ratio >= 0.65 ? 'text-emerald-700 bg-emerald-50' : 'text-amber-700 bg-amber-50',
      tooltip: `Current thermal efficiency is ${(metadata.thermal_ratio * 100).toFixed(1)}%. Minimum recommended efficiency is 65% for optimal energy utilization.`,
      isEfficiencyMetric: true
    }
  ];

  const maxValue = Math.max(...consumptionData.map(d => d.value));

  return (
    <Card>
      <CardHeader className="space-y-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <CardTitle>Resource Consumption Analysis</CardTitle>
            <Tooltip>
              <TooltipTrigger>
                <HelpCircle className="h-4 w-4 text-muted-foreground" />
              </TooltipTrigger>
              <TooltipContent>
                <p className="max-w-xs">
                  Comprehensive analysis of resource usage in the RF treatment process, including electricity, water, cooling, and thermal efficiency metrics. Values are calculated based on a total process mass of {metadata.total_mass.toFixed(0)} kg.
                </p>
              </TooltipContent>
            </Tooltip>
          </div>
          <div className="flex items-center gap-2">
            <span className="text-sm font-medium bg-blue-50 text-blue-700 px-2 py-1 rounded">
              RF Treatment Process
            </span>
            <Tooltip>
              <TooltipTrigger>
                <HelpCircle className="h-4 w-4 text-muted-foreground" />
              </TooltipTrigger>
              <TooltipContent>
                <p className="max-w-xs">
                  Radio Frequency treatment process operating at 27.12 MHz with conveyor speed 0.17 m/min and electrode gap 86.9 mm.
                </p>
              </TooltipContent>
            </Tooltip>
          </div>
        </div>
        
        <div className="grid grid-cols-2 gap-4 text-sm">
          <div className="bg-gray-50 p-3 rounded">
            <div className="flex items-center gap-2">
              <div className="text-gray-600 mb-1">Process Parameters</div>
              <Tooltip>
                <TooltipTrigger>
                  <HelpCircle className="h-4 w-4 text-muted-foreground" />
                </TooltipTrigger>
                <TooltipContent>
                  <p className="max-w-xs">
                    Key process parameters that affect resource consumption and efficiency. Total mass represents the amount of material being processed in this batch.
                  </p>
                </TooltipContent>
              </Tooltip>
            </div>
            <div className="space-y-1">
              <div className="flex justify-between">
                <span>Total Mass:</span>
                <span className="font-medium">{metadata.total_mass.toFixed(0)} kg</span>
              </div>
            </div>
          </div>
          <div className="bg-gray-50 p-3 rounded">
            <div className="flex items-center gap-2">
              <div className="text-gray-600 mb-1">Current Intensities</div>
              <Tooltip>
                <TooltipTrigger>
                  <HelpCircle className="h-4 w-4 text-muted-foreground" />
                </TooltipTrigger>
                <TooltipContent>
                  <p className="max-w-xs">
                    Resource consumption per kg of processed material. Energy intensity shows power usage efficiency, while water intensity indicates water usage efficiency. Lower values indicate better resource utilization.
                  </p>
                </TooltipContent>
              </Tooltip>
            </div>
            <div className="space-y-1">
              <div className="flex justify-between items-center">
                <div className="flex items-center gap-1">
                  <span>Energy:</span>
                  <Tooltip>
                    <TooltipTrigger>
                      <HelpCircle className="h-3 w-3 text-muted-foreground" />
                    </TooltipTrigger>
                    <TooltipContent>
                      <p className="max-w-xs">
                        Total electrical energy consumed per kg of processed material. Target: ≤0.65 kWh/kg for optimal energy efficiency.
                      </p>
                    </TooltipContent>
                  </Tooltip>
                </div>
                <span className="font-medium">{metadata.energy_intensity.toFixed(2)} kWh/kg</span>
              </div>
              <div className="flex justify-between items-center">
                <div className="flex items-center gap-1">
                  <span>Water:</span>
                  <Tooltip>
                    <TooltipTrigger>
                      <HelpCircle className="h-3 w-3 text-muted-foreground" />
                    </TooltipTrigger>
                    <TooltipContent>
                      <p className="max-w-xs">
                        Total water consumed per kg of processed material. Target: ≤0.55 kg/kg for optimal water efficiency.
                      </p>
                    </TooltipContent>
                  </Tooltip>
                </div>
                <span className="font-medium">{metadata.water_intensity.toFixed(2)} kg/kg</span>
              </div>
            </div>
          </div>
        </div>
      </CardHeader>

      <CardContent className="space-y-6">
        {consumptionData.map((item) => (
          <div key={item.name} className="rounded-lg border p-4 space-y-3">
            <div className="flex items-center gap-3">
              <Tooltip>
                <TooltipTrigger>
                  <div className={`rounded-full p-2.5 ${item.bgColor} ${item.textColor}`}>
                    {item.icon}
                  </div>
                </TooltipTrigger>
                <TooltipContent>
                  <p className="max-w-xs">
                    {item.name === 'Electricity' && 'Total electrical energy consumed by the RF treatment process, including power for heating and mechanical operations.'}
                    {item.name === 'Process Water' && 'Water used for tempering and cleaning processes, excluding cooling water consumption.'}
                    {item.name === 'Cooling System' && 'Water required for temperature control in the RF treatment process. Lower values indicate better cooling efficiency.'}
                    {item.name === 'Thermal Efficiency' && 'Ratio of useful heat output to total energy input. Higher values indicate better energy utilization.'}
                  </p>
                </TooltipContent>
              </Tooltip>
              <div className="flex-1">
                <div className="flex items-start justify-between">
                  <div>
                    <div className="flex items-center gap-2">
                      <h3 className="font-medium text-base">{item.name}</h3>
                      <Tooltip>
                        <TooltipTrigger>
                          <HelpCircle className="h-4 w-4 text-muted-foreground" />
                        </TooltipTrigger>
                        <TooltipContent>
                          <p className="max-w-xs">
                            {item.name === 'Electricity' && `Current consumption: ${item.value.toFixed(1)} ${item.unit} (${item.benchmark ? ((item.value / item.benchmark) * 100).toFixed(1) : 'N/A'}% of maximum allowable)`}
                            {item.name === 'Process Water' && `Current usage: ${item.value.toFixed(1)} ${item.unit} (${item.benchmark ? ((item.value / item.benchmark) * 100).toFixed(1) : 'N/A'}% of maximum allowable)`}
                            {item.name === 'Cooling System' && `Cooling efficiency: ${item.value.toFixed(1)} ${item.unit} of cooling water per kWh of RF energy`}
                            {item.name === 'Thermal Efficiency' && `Current efficiency: ${item.value.toFixed(1)}% (Target: ≥${item.benchmark}% for optimal energy utilization)`}
                          </p>
                        </TooltipContent>
                      </Tooltip>
                    </div>
                    <p className="text-sm text-gray-600">
                      {item.description}
                    </p>
                  </div>
                  <div className="text-right">
                    <div className="flex items-center gap-2 justify-end">
                      <p className="text-lg font-semibold">
                        {item.value.toFixed(1)} {item.unit}
                      </p>
                      <Tooltip>
                        <TooltipTrigger>
                          <HelpCircle className="h-4 w-4 text-muted-foreground" />
                        </TooltipTrigger>
                        <TooltipContent>
                          <p className="max-w-xs">
                            {item.name === 'Electricity' && `Based on total energy consumption across all process steps. Maximum allowable: ${item.benchmark?.toFixed(1)} ${item.unit}`}
                            {item.name === 'Process Water' && `Includes water for tempering and cleaning. Maximum allowable: ${item.benchmark?.toFixed(1)} ${item.unit}`}
                            {item.name === 'Cooling System' && 'Lower values indicate more efficient cooling system performance'}
                            {item.name === 'Thermal Efficiency' && `Higher values indicate better energy utilization. Minimum target: ${item.benchmark}%`}
                          </p>
                        </TooltipContent>
                      </Tooltip>
                    </div>
                    {item.benchmark && !item.isEfficiencyMetric && (
                      <p className="text-sm text-gray-600">
                        Maximum: {item.benchmark.toFixed(1)} {item.unit}
                      </p>
                    )}
                    {item.benchmark && item.isEfficiencyMetric && (
                      <p className="text-sm text-gray-600">
                        Target: ≤{item.benchmark} {item.unit}
                      </p>
                    )}
                  </div>
                </div>
                
                {item.status && (
                  <div className="mt-2 flex items-center gap-2">
                    <span className={`inline-flex items-center px-2 py-0.5 rounded text-xs font-medium ${item.statusColor}`}>
                      {item.status}
                    </span>
                    <Tooltip>
                      <TooltipTrigger className="group">
                        <div className="text-xs text-gray-500 group-hover:text-gray-900 cursor-help underline decoration-dotted">
                          More Info
                        </div>
                      </TooltipTrigger>
                      <TooltipContent>
                        <p className="max-w-xs">
                          {item.tooltip}
                        </p>
                      </TooltipContent>
                    </Tooltip>
                  </div>
                )}
              </div>
            </div>

            {item.benchmark ? (
              <div className="space-y-2">
                <div className="flex justify-between text-xs text-gray-600">
                  <div className="flex items-center gap-1">
                    <span>{item.isEfficiencyMetric ? 'Current Efficiency' : 'Current Usage'}</span>
                    <Tooltip>
                      <TooltipTrigger>
                        <HelpCircle className="h-3 w-3 text-muted-foreground" />
                      </TooltipTrigger>
                      <TooltipContent>
                        <p className="max-w-xs">
                          {item.isEfficiencyMetric 
                            ? `Current performance relative to target efficiency of ${item.benchmark}${item.unit}`
                            : `Current consumption relative to maximum allowable of ${item.benchmark.toFixed(1)} ${item.unit}`}
                        </p>
                      </TooltipContent>
                    </Tooltip>
                  </div>
                  <div className="flex items-center gap-1">
                    <span>{item.isEfficiencyMetric ? 'Target' : 'Limit'}</span>
                    <Tooltip>
                      <TooltipTrigger>
                        <HelpCircle className="h-3 w-3 text-muted-foreground" />
                      </TooltipTrigger>
                      <TooltipContent>
                        <p className="max-w-xs">
                          {item.isEfficiencyMetric 
                            ? 'Minimum required efficiency for optimal process performance'
                            : 'Maximum allowable consumption for sustainable operation'}
                        </p>
                      </TooltipContent>
                    </Tooltip>
                  </div>
                </div>
                <div className="relative h-3 bg-gray-100 rounded-full">
                  <div 
                    className={`absolute h-full rounded-full ${
                      item.isEfficiencyMetric 
                        ? (
                            item.value >= item.benchmark ? 'bg-emerald-500' : 
                            item.value >= item.benchmark * 0.9 ? 'bg-amber-500' : 
                            'bg-red-500'
                          )
                        : (
                            item.value <= item.benchmark * 0.9 ? 'bg-emerald-500' :
                            item.value <= item.benchmark ? 'bg-amber-500' :
                            'bg-red-500'
                          )
                    }`}
                    style={{ 
                      width: item.isEfficiencyMetric
                        ? `${Math.min((item.value / item.benchmark) * 100, 100)}%`
                        : `${Math.min((item.value / item.benchmark) * 100, 100)}%`,
                      opacity: 0.8
                    }}
                  />
                  <div 
                    className="absolute h-full w-0.5 bg-gray-400"
                    style={{ 
                      left: '100%',
                      transform: 'translateX(-2px)'
                    }}
                  />
                </div>
                <div className="flex justify-between text-xs">
                  <span className={
                    item.isEfficiencyMetric
                      ? (
                          item.value >= item.benchmark ? 'text-emerald-700' :
                          item.value >= item.benchmark * 0.9 ? 'text-amber-700' :
                          'text-red-700'
                        )
                      : (
                          item.value <= item.benchmark * 0.9 ? 'text-emerald-700' :
                          item.value <= item.benchmark ? 'text-amber-700' :
                          'text-red-700'
                        )
                  }>
                    {item.isEfficiencyMetric 
                      ? `${((item.value / item.benchmark) * 100).toFixed(0)}% of target`
                      : `${((item.value / item.benchmark) * 100).toFixed(0)}% of limit`
                    }
                  </span>
                </div>
              </div>
            ) : (
              <div className="mt-2">
                <p className="text-sm text-gray-600">{item.tooltip}</p>
              </div>
            )}
          </div>
        ))}
      </CardContent>
    </Card>
  );
} 