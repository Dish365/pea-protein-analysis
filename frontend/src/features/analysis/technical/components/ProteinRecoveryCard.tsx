"use client";

import React from 'react';
import { Beaker, Percent, Scissors } from 'lucide-react';
import { Progress } from "@/components/ui/progress";
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

interface ProteinRecoveryCardProps {
  massRecovery: number;
  contentRecovery: number;
  yieldRecovery: number;
}

export function ProteinRecoveryCard({
  massRecovery,
  contentRecovery,
  yieldRecovery,
}: ProteinRecoveryCardProps) {
  const metrics = [
    {
      title: 'Mass Recovery',
      value: massRecovery,
      icon: <Beaker className="h-4 w-4" />,
      suffix: '%',
      tooltip: 'Percentage of protein mass recovered',
      threshold: 90,
    },
    {
      title: 'Content Recovery',
      value: contentRecovery,
      icon: <Percent className="h-4 w-4" />,
      suffix: '%',
      tooltip: 'Protein content in recovered material',
      threshold: 95,
    },
    {
      title: 'Yield Recovery',
      value: yieldRecovery,
      icon: <Scissors className="h-4 w-4" />,
      suffix: '%',
      tooltip: 'Overall protein yield efficiency',
      threshold: 85,
    },
  ];

  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
        <CardTitle>Protein Recovery Analysis</CardTitle>
        <TooltipProvider>
          <Tooltip>
            <TooltipTrigger asChild>
              <Badge
                variant={yieldRecovery >= 85 ? "success" : "warning"}
              >
                {yieldRecovery >= 85 ? 'Optimal' : 'Suboptimal'}
              </Badge>
            </TooltipTrigger>
            <TooltipContent>
              <p>Overall recovery performance</p>
            </TooltipContent>
          </Tooltip>
        </TooltipProvider>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {metrics.map((metric, index) => (
            <TooltipProvider key={index}>
              <Tooltip>
                <TooltipTrigger asChild>
                  <Card>
                    <CardContent className="pt-6">
                      <div className="flex items-center gap-2">
                        <div
                          className={`rounded-full p-2 ${
                            metric.value >= metric.threshold
                              ? 'bg-emerald-100 text-emerald-700'
                              : 'bg-blue-100 text-blue-700'
                          }`}
                        >
                          {metric.icon}
                        </div>
                        <div className="flex-1">
                          <p className="text-sm font-medium text-muted-foreground">
                            {metric.title}
                          </p>
                          <p
                            className={`text-2xl font-bold ${
                              metric.value >= metric.threshold
                                ? 'text-emerald-600'
                                : 'text-blue-600'
                            }`}
                          >
                            {metric.value.toFixed(1)}{metric.suffix}
                          </p>
                        </div>
                      </div>
                      <div className="mt-4">
                        <Progress
                          value={Math.min(100, Math.max(0, metric.value))}
                          className={metric.value >= metric.threshold ? 'bg-emerald-100' : 'bg-blue-100'}
                          indicatorColor={
                            metric.value >= metric.threshold
                              ? 'rgb(16 185 129)'  // emerald-500
                              : 'rgb(59 130 246)'  // blue-500
                          }
                        />
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