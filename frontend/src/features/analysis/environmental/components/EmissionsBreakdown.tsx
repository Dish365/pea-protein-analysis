"use client";

import React from 'react';
import { Zap, Droplets, TestTubes } from 'lucide-react';
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
import { Separator } from "@/components/ui/separator";

interface EmissionsBreakdownProps {
  impactAssessment: {
    gwp: number;
    hct: number;
    frs: number;
  };
  processType: string;
}

export function EmissionsBreakdown({ 
  impactAssessment,
  processType 
}: EmissionsBreakdownProps) {
  const metrics = [
    {
      key: 'gwp',
      label: 'Global Warming Potential',
      value: impactAssessment.gwp,
      icon: <Zap className="h-4 w-4" />,
      color: 'rgb(59 130 246)', // blue-500
      bgColor: 'bg-blue-100',
      textColor: 'text-blue-700',
      unit: 'kg CO₂eq',
      description: 'Carbon dioxide equivalent emissions'
    },
    {
      key: 'hct',
      label: 'Human Carcinogenic Toxicity',
      value: impactAssessment.hct,
      icon: <TestTubes className="h-4 w-4" />,
      color: 'rgb(147 51 234)', // purple-500
      bgColor: 'bg-purple-100',
      textColor: 'text-purple-700',
      unit: 'CTUh',
      description: 'Comparative Toxic Units for human health'
    },
    {
      key: 'frs',
      label: 'Fossil Resource Scarcity',
      value: impactAssessment.frs,
      icon: <Droplets className="h-4 w-4" />,
      color: 'rgb(34 211 238)', // cyan-500
      bgColor: 'bg-cyan-100',
      textColor: 'text-cyan-700',
      unit: 'kg oil eq',
      description: 'Oil equivalent of fossil resources used'
    }
  ];

  const totalImpact = Object.values(impactAssessment).reduce((a, b) => a + b, 0);

  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
        <CardTitle>Environmental Impact Assessment</CardTitle>
        <Badge variant="outline" className="font-mono">
          {processType.toUpperCase()}
        </Badge>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {metrics.map(metric => {
            const percentage = (metric.value / totalImpact) * 100;
            return (
              <TooltipProvider key={metric.key}>
                <Tooltip>
                  <TooltipTrigger asChild>
                    <div className="space-y-2">
                      <div className="flex items-center justify-between">
                        <div className="flex items-center gap-2">
                          <div className={`rounded-full p-2 ${metric.bgColor} ${metric.textColor}`}>
                            {metric.icon}
                          </div>
                          <span className="font-medium">{metric.label}</span>
                        </div>
                        <span className="font-medium">
                          {formatNumber(metric.value)} {metric.unit}
                        </span>
                      </div>
                      <Progress
                        value={percentage}
                        className={metric.bgColor}
                        indicatorColor={metric.color}
                      />
                    </div>
                  </TooltipTrigger>
                  <TooltipContent>
                    <p>{metric.description}</p>
                  </TooltipContent>
                </Tooltip>
              </TooltipProvider>
            );
          })}
        </div>

        <Separator className="my-6" />

        <div className="text-center space-y-2">
          <TooltipProvider>
            <Tooltip>
              <TooltipTrigger>
                <div>
                  <p className="text-sm font-medium text-muted-foreground">
                    Total Impact Score
                  </p>
                  <p className="text-3xl font-bold text-primary">
                    {formatNumber(totalImpact)}
                  </p>
                </div>
              </TooltipTrigger>
              <TooltipContent>
                <p>Total environmental impact score</p>
              </TooltipContent>
            </Tooltip>
          </TooltipProvider>
        </div>
      </CardContent>
    </Card>
  );
} 