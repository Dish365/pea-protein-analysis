"use client";

import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { ConsumptionMetrics } from '@/types/environmental';
import { Zap, Droplets, Snowflake } from 'lucide-react';
import { Progress } from "@/components/ui/progress";

interface ResourceConsumptionProps {
  metrics: ConsumptionMetrics;
  efficiency: number;
}

export function ResourceConsumption({
  metrics,
  efficiency,
}: ResourceConsumptionProps) {
  const consumptionData = [
    {
      name: 'Electricity',
      value: metrics.electricity,
      unit: 'kWh',
      icon: <Zap className="h-4 w-4" />,
      color: 'rgb(234 179 8)', // yellow-500
      description: 'Total electricity consumption',
    },
    {
      name: 'Water',
      value: metrics.water,
      unit: 'm³',
      icon: <Droplets className="h-4 w-4" />,
      color: 'rgb(59 130 246)', // blue-500
      description: 'Total water consumption',
    },
    {
      name: 'Cooling',
      value: metrics.cooling,
      unit: 'kWh',
      icon: <Snowflake className="h-4 w-4" />,
      color: 'rgb(99 102 241)', // indigo-500
      description: 'Total cooling energy consumption',
    },
  ].filter((item) => item.value !== null);

  return (
    <Card>
      <CardHeader>
        <CardTitle>Resource Consumption</CardTitle>
        <p className="text-sm text-muted-foreground">
          Energy Efficiency: {efficiency.toFixed(1)}%
        </p>
      </CardHeader>
      <CardContent className="space-y-6">
        {consumptionData.map((item) => (
          <div key={item.name} className="space-y-2">
            <div className="flex items-center gap-2">
              <div className={`rounded-full p-2 bg-${item.color.split(' ')[1]}/20`}>
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
              value={item.value / Math.max(...consumptionData.map(d => d.value || 0)) * 100}
              className="h-2"
            />
          </div>
        ))}
      </CardContent>
    </Card>
  );
} 