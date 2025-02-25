"use client";

import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { Zap, Recycle, Leaf, AlertTriangle, CheckCircle2, HelpCircle } from 'lucide-react';
import { ImpactResults } from '@/types/environmental';
import { Tooltip, TooltipContent, TooltipTrigger } from "@/components/ui/tooltip";

interface SustainabilityScoreProps {
  impactResults: ImpactResults;
}

export function SustainabilityScore({
  impactResults,
}: SustainabilityScoreProps) {
  const { metadata, rf_parameters } = impactResults;
  const rf_validation = impactResults.rf_validation || {
    temperature: {
      outfeed: {
        value: rf_parameters.temperature_outfeed,
        within_range: rf_parameters.temperature_outfeed >= 80 && rf_parameters.temperature_outfeed <= 90,
        optimal: 84.4,
        tolerance: "±5°C"
      },
      electrode: {
        value: rf_parameters.temperature_electrode,
        within_range: rf_parameters.temperature_electrode >= 95 && rf_parameters.temperature_electrode <= 105,
        optimal: 100.1,
        tolerance: "±5°C"
      }
    },
    moisture: {
      initial: metadata.initial_moisture || 0.136,
      final: metadata.final_moisture || 0.102,
      target: metadata.target_moisture || 0.125,
      reduction: 0.034,
      within_range: true,
      optimal_reduction: 0.034,
      tolerance: "±0.005"
    },
    energy_efficiency: {
      value: rf_parameters.contribution_percentage / 100,
      within_range: Math.abs(rf_parameters.contribution_percentage - 19) <= 1,
      optimal: 0.19,
      tolerance: "±0.01"
    }
  };

  // Update the metrics with research-based targets
  const metrics = [
    {
      label: "RF Treatment Efficiency",
      value: rf_parameters.contribution_percentage,
      icon: <Recycle className="h-4 w-4" />,
      description: "RF heating system performance",
      target: 19,
      validation: {
        status: rf_validation.energy_efficiency.within_range,
        message: rf_validation.energy_efficiency.within_range ? 
          "RF energy contribution within optimal range" :
          `RF energy contribution (${rf_parameters.contribution_percentage.toFixed(1)}%) below research target (19±1%)`,
        current: `${rf_parameters.contribution_percentage.toFixed(1)}%`,
        optimal: "19±1%",
        details: [
          `Temperature Control: ${rf_parameters.temperature_outfeed.toFixed(1)}°C (Target: 84.4±5°C)`,
          `Protein Yield: ${((metadata.mass_flows.protein_concentrate / metadata.total_mass) * 100).toFixed(1)}% (Target: 21.9%)`,
          `Moisture Reduction: ${((rf_validation.moisture.initial - rf_validation.moisture.final) * 100).toFixed(1)}%`
        ]
      }
    },
    {
      label: "Process Efficiency",
      value: (metadata.mass_flows.protein_concentrate / metadata.total_mass) * 100,
      icon: <Zap className="h-4 w-4" />,
      description: "Protein extraction efficiency",
      target: 21.9, // Research benchmark
      validation: {
        status: (metadata.mass_flows.protein_concentrate / metadata.total_mass) >= 0.219,
        message: "Protein yield should meet research benchmark of 21.9%",
        current: `${((metadata.mass_flows.protein_concentrate / metadata.total_mass) * 100).toFixed(1)}%`,
        optimal: "21.9%",
        details: [
          `Protein Concentrate: ${metadata.mass_flows.protein_concentrate.toFixed(1)} kg`,
          `Total Mass: ${metadata.total_mass.toFixed(1)} kg`,
          `Target Range: 21.9±2%`
        ]
      }
    },
    {
      label: "Energy Efficiency",
      value: (1 - metadata.energy_intensity) * 100,
      icon: <Zap className="h-4 w-4" />,
      description: "Process energy utilization efficiency",
      target: 80,
      validation: {
        status: metadata.energy_intensity <= 0.65,
        message: "Energy intensity should be below 0.65 kWh/kg",
        current: `${metadata.energy_intensity.toFixed(2)} kWh/kg`,
        optimal: "0.65 kWh/kg",
        details: [
          `Total Energy: ${(metadata.energy_intensity * metadata.total_mass).toFixed(1)} kWh`,
          `Specific Consumption: ${metadata.energy_intensity.toFixed(2)} kWh/kg`,
          `Target Range: ≤ 0.65 kWh/kg`
        ]
      }
    },
    {
      label: "Resource Conservation",
      value: (1 - metadata.water_intensity) * 100,
      icon: <Leaf className="h-4 w-4" />,
      description: "Water and material utilization efficiency",
      target: 70,
      validation: {
        status: metadata.water_intensity <= 0.55,
        message: "Water intensity should be below 0.55 kg/kg",
        current: `${metadata.water_intensity.toFixed(2)} kg/kg`,
        optimal: "0.55 kg/kg",
        details: [
          `Water Usage: ${(metadata.water_intensity * metadata.total_mass).toFixed(1)} kg`,
          `Specific Consumption: ${metadata.water_intensity.toFixed(2)} kg/kg`,
          `Target Range: ≤ 0.55 kg/kg`
        ]
      }
    },
  ];

  // Update validation issues to include protein yield
  const validationIssues = [
    !rf_validation.energy_efficiency.within_range && 
      `RF energy contribution (${rf_parameters.contribution_percentage.toFixed(1)}%) below target (19±1%)`,
    (metadata.mass_flows.protein_concentrate / metadata.total_mass) < 0.219 && 
      `Protein yield (${((metadata.mass_flows.protein_concentrate / metadata.total_mass) * 100).toFixed(1)}%) below benchmark (21.9%)`,
    metadata.energy_intensity > 0.65 && 
      `High energy intensity (${metadata.energy_intensity.toFixed(2)} kWh/kg)`,
    !rf_validation.temperature.outfeed.within_range && 
      `Temperature control issue (${rf_parameters.temperature_outfeed.toFixed(1)}°C)`
  ].filter(Boolean);

  // Update the weighted score calculation
  const weights = { 
    rf: 0.35,       // RF treatment is critical for protein yield
    process: 0.35,  // Process efficiency (protein yield)
    energy: 0.20,   // Energy efficiency
    resource: 0.10  // Resource conservation
  };

  const overallScore = (
    // RF Treatment Efficiency
    (metrics[0].value / metrics[0].target) * weights.rf +
    // Process Efficiency (Protein Yield)
    (metrics[1].value / metrics[1].target) * weights.process +
    // Energy Efficiency
    (metrics[2].value / metrics[2].target) * weights.energy +
    // Resource Conservation
    (metrics[3].value / metrics[3].target) * weights.resource
  ) * 100;

  return (
    <Card>
      <CardHeader>
        <div className="flex items-center justify-between">
          <div>
            <CardTitle>Process Sustainability Assessment</CardTitle>
            <p className="text-sm text-muted-foreground mt-1">
              Overall performance score based on key efficiency metrics
            </p>
          </div>
          <div className="text-right">
            <div className="flex items-center gap-2">
              <span className={`text-3xl font-bold ${
                overallScore >= 90 ? 'text-green-600' :
                overallScore >= 70 ? 'text-blue-600' :
                'text-yellow-600'
              }`}>
                {overallScore.toFixed(1)}%
              </span>
              <Tooltip>
                <TooltipTrigger>
                  <HelpCircle className="h-4 w-4 text-muted-foreground" />
                </TooltipTrigger>
                <TooltipContent>
                  <p className="max-w-xs">
                    Weighted score based on research priorities:
                    <br/>• RF Treatment (35%)
                    <br/>• Protein Yield (35%)
                    <br/>• Energy Efficiency (20%)
                    <br/>• Resource Conservation (10%)
                  </p>
                </TooltipContent>
              </Tooltip>
            </div>
          </div>
        </div>
      </CardHeader>
      <CardContent className="space-y-6">
        {/* Key Performance Metrics */}
        {metrics.map((metric) => {
          const performance = (metric.value / metric.target) * 100;
          return (
            <div key={metric.label} className="space-y-2">
              <div className="flex items-center gap-2">
                <div className={`rounded-full p-2 ${
                  metric.validation.status ? 'bg-green-100 text-green-700' : 'bg-yellow-100 text-yellow-700'
                }`}>
                  {metric.icon}
                </div>
                <div className="flex-1">
                  <div className="flex items-center gap-2">
                    <p className="font-medium">{metric.label}</p>
                    <Tooltip>
                      <TooltipTrigger>
                        {metric.validation.status ? 
                          <CheckCircle2 className="h-4 w-4 text-green-500" /> :
                          <AlertTriangle className="h-4 w-4 text-yellow-500" />
                        }
                      </TooltipTrigger>
                      <TooltipContent>
                        <p>{metric.validation.message}</p>
                        <p className="text-sm mt-1">
                          Current: {metric.validation.current}
                          <br />
                          Optimal: {metric.validation.optimal}
                        </p>
                      </TooltipContent>
                    </Tooltip>
                  </div>
                  <p className="text-sm text-muted-foreground">
                    {metric.description}
                  </p>
                </div>
                <div className="text-right">
                  <p className={`text-lg font-semibold ${
                    metric.validation.status ? 'text-green-600' : 'text-yellow-600'
                  }`}>
                    {metric.value.toFixed(1)}%
                  </p>
                </div>
              </div>
              <Progress
                value={performance}
                className={`h-2 ${
                  metric.validation.status ? 'bg-green-100' : 'bg-yellow-100'
                }`}
              />
            </div>
          );
        })}

        {/* Validation Summary */}
        {validationIssues.length > 0 && (
          <div className="mt-6 p-4 bg-yellow-50 rounded-lg border border-yellow-200">
            <div className="flex items-center gap-2 mb-2">
              <AlertTriangle className="h-5 w-5 text-yellow-600" />
              <h4 className="font-medium text-yellow-900">Improvement Opportunities</h4>
            </div>
            <ul className="list-disc list-inside text-sm text-yellow-800 space-y-1">
              {validationIssues.map((issue, index) => (
                <li key={index}>{issue}</li>
              ))}
            </ul>
          </div>
        )}
      </CardContent>
    </Card>
  );
} 