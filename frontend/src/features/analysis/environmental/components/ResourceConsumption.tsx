"use client";

import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { ImpactResults } from '@/types/environmental';
import { Zap, Droplets, Snowflake, Factory } from 'lucide-react';
import { Progress } from "@/components/ui/progress";

interface ResourceConsumptionProps {
  impactResults: ImpactResults;
}

export function ResourceConsumption({
  impactResults,
}: ResourceConsumptionProps) {
  const { process_contributions, metadata } = impactResults;

  const consumptionData = [
    {
      name: 'Electricity',
      value: process_contributions.gwp.electricity.value,
      unit: process_contributions.gwp.electricity.unit,
      icon: <Zap className="h-4 w-4" />,
      color: 'yellow',
      description: 'Total electricity consumption',
    },
    {
      name: 'Water',
      value: process_contributions.water.tempering.value + process_contributions.water.cleaning.value,
      unit: 'kg',
      icon: <Droplets className="h-4 w-4" />,
      color: 'blue',
      description: 'Total water consumption',
    },
    {
      name: 'Cooling',
      value: process_contributions.water.cooling.value,
      unit: process_contributions.water.cooling.unit,
      icon: <Snowflake className="h-4 w-4" />,
      color: 'indigo',
      description: 'Cooling energy consumption',
    },
    {
      name: 'Thermal',
      value: process_contributions.frs.thermal_treatment.value,
      unit: process_contributions.frs.thermal_treatment.unit,
      icon: <Factory className="h-4 w-4" />,
      color: 'red',
      description: 'Thermal energy consumption',
    },
  ];

  const maxValue = Math.max(...consumptionData.map(d => d.value));

  return (
    <Card>
      <CardHeader>
        <CardTitle>Resource Consumption</CardTitle>
        <div className="flex items-center justify-between">
          <p className="text-sm text-muted-foreground">
            Energy Intensity: {metadata.energy_intensity.toFixed(2)} kWh/kg
          </p>
          <p className="text-sm text-muted-foreground">
            Water Intensity: {metadata.water_intensity.toFixed(2)} kg/kg
          </p>
        </div>
      </CardHeader>
      <CardContent className="space-y-6">
        {consumptionData.map((item) => (
          <div key={item.name} className="space-y-2">
            <div className="flex items-center gap-2">
              <div className={`rounded-full p-2 bg-${item.color}-100 text-${item.color}-700`}>
                {item.icon}
              </div>
              <div>
                <p className="font-medium">{item.name}</p>
                <p className="text-sm text-muted-foreground">
                  {item.description}
                </p>
              </div>
              <div className="ml-auto text-right">
                <p className="text-lg font-semibold">
                  {item.value.toFixed(1)} {item.unit}
                </p>
              </div>
            </div>
            <Progress
              value={(item.value / maxValue) * 100}
              className={`h-2 bg-${item.color}-100`}
            />
          </div>
        ))}
      </CardContent>
    </Card>
  );
} 