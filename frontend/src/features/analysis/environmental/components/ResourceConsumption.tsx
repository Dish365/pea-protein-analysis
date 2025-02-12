"use client";

import React from 'react';
import { Zap, Droplet, Snowflake } from 'lucide-react';
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
import { Progress } from "@/components/ui/progress";
import { Badge } from "@/components/ui/badge";

interface ResourceConsumptionProps {
  consumptionMetrics: {
    electricity: number | null;
    cooling: number | null;
    water: number | null;
  };
  processType: string;
}

export function ResourceConsumption({ 
  consumptionMetrics,
  processType 
}: ResourceConsumptionProps) {
  const metrics = [
    {
      key: 'electricity',
      title: 'Electricity Consumption',
      value: consumptionMetrics.electricity,
      suffix: 'kWh',
      icon: <Zap className="h-4 w-4" />,
      tooltip: 'Total electrical energy consumed',
      color: 'rgb(59 130 246)', // blue-500
      bgColor: 'bg-blue-100',
      textColor: 'text-blue-700',
      visible: processType === 'rf'
    },
    {
      key: 'cooling',
      title: 'Cooling Energy',
      value: consumptionMetrics.cooling,
      suffix: 'kWh',
      icon: <Snowflake className="h-4 w-4" />,
      tooltip: 'Total cooling energy required',
      color: 'rgb(34 211 238)', // cyan-500
      bgColor: 'bg-cyan-100',
      textColor: 'text-cyan-700',
      visible: processType === 'ir'
    },
    {
      key: 'water',
      title: 'Water Usage',
      value: consumptionMetrics.water,
      suffix: 'm³',
      icon: <Droplet className="h-4 w-4" />,
      tooltip: 'Total water consumption',
      color: 'rgb(34 197 94)', // green-500
      bgColor: 'bg-green-100',
      textColor: 'text-green-700',
      visible: true
    }
  ].filter(metric => metric.visible);

  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
        <CardTitle>Resource Consumption</CardTitle>
        <Badge variant="outline" className="font-mono">
          {processType.toUpperCase()}
        </Badge>
      </CardHeader>
      <CardContent>
        <div className="grid gap-4 md:grid-cols-2">
          {metrics.map(metric => (
            <TooltipProvider key={metric.key}>
              <Tooltip>
                <TooltipTrigger asChild>
                  <Card>
                    <CardContent className="pt-6">
                      <div className="space-y-2">
                        <div className="flex items-center justify-between">
                          <div className="flex items-center gap-2">
                            <div className={`rounded-full p-2 ${metric.bgColor} ${metric.textColor}`}>
                              {metric.icon}
                            </div>
                            <span className="font-medium">{metric.title}</span>
                          </div>
                          <span className="font-medium">
                            {metric.value !== null ? `${formatNumber(metric.value)} ${metric.suffix}` : 'N/A'}
                          </span>
                        </div>
                        {metric.value !== null && (
                          <Progress
                            value={75} // You can calculate this based on benchmarks
                            className={metric.bgColor}
                            indicatorColor={metric.color}
                          />
                        )}
                      </div>
                    </CardContent>
                  </Card>
                </TooltipTrigger>
                <TooltipContent>
                  <p>{metric.tooltip}</p>
                </TooltipContent>
              </Tooltip>
            </TooltipProvider>
          ))}
        </div>
      </CardContent>
    </Card>
  );
} 