"use client";

import React from 'react';
import { AlertCircle, CheckCircle } from 'lucide-react';
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

interface SustainabilityScoreProps {
  impacts: {
    gwp: number;
    hct: number;
    frs: number;
  };
  processType: string;
}

export function SustainabilityScore({ impacts, processType }: SustainabilityScoreProps) {
  const calculateMetrics = () => {
    const benchmarks = {
      baseline: { gwp: 100, hct: 0.1, frs: 50 },
      rf: { gwp: 90, hct: 0.08, frs: 45 },
      ir: { gwp: 95, hct: 0.09, frs: 47 }
    };

    const benchmark = benchmarks[processType as keyof typeof benchmarks] || benchmarks.baseline;
    
    const gwpScore = Math.max(0, 100 * (1 - impacts.gwp / benchmark.gwp));
    const hctScore = Math.max(0, 100 * (1 - impacts.hct / benchmark.hct));
    const frsScore = Math.max(0, 100 * (1 - impacts.frs / benchmark.frs));

    const sustainabilityScore = (gwpScore + hctScore + frsScore) / 3;
    const circularityIndex = Math.min(1, Math.max(0, 1 - (impacts.frs / benchmark.frs)));
    const resourceEfficiency = Math.min(100, Math.max(0, 100 * (1 - impacts.gwp / benchmark.gwp)));

    return {
      sustainabilityScore,
      circularityIndex,
      resourceEfficiency
    };
  };

  const metrics = calculateMetrics();

  const getScoreColor = (score: number) => {
    if (score >= 70) return 'rgb(34 197 94)'; // green-500
    if (score >= 50) return 'rgb(234 179 8)'; // yellow-500
    return 'rgb(239 68 68)'; // red-500
  };

  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
        <CardTitle>Sustainability Assessment</CardTitle>
        <Badge variant="outline" className="font-mono">
          {processType.toUpperCase()}
        </Badge>
      </CardHeader>
      <CardContent>
        <div className="space-y-6">
          <TooltipProvider>
            <Tooltip>
              <TooltipTrigger asChild>
                <div className="text-center space-y-4">
                  <div className="relative h-32 w-32 mx-auto">
                    <Progress
                      value={Math.round(metrics.sustainabilityScore)}
                      indicatorColor={getScoreColor(metrics.sustainabilityScore)}
                      className="h-32 w-32 rounded-full"
                    />
                    <div className="absolute inset-0 flex flex-col items-center justify-center">
                      <span className="text-3xl font-bold">
                        {formatNumber(metrics.sustainabilityScore)}
                      </span>
                      <span className="text-sm text-muted-foreground">
                        Score
                      </span>
                    </div>
                  </div>
                </div>
              </TooltipTrigger>
              <TooltipContent>
                <p>Overall sustainability score based on environmental impacts</p>
              </TooltipContent>
            </Tooltip>
          </TooltipProvider>

          <div className="grid gap-4 md:grid-cols-2">
            <TooltipProvider>
              <Tooltip>
                <TooltipTrigger asChild>
                  <Card>
                    <CardContent className="pt-6">
                      <div className="text-center">
                        <p className="text-sm font-medium text-muted-foreground">
                          Circularity Index
                        </p>
                        <p className="text-2xl font-bold" style={{ color: getScoreColor(metrics.circularityIndex * 100) }}>
                          {metrics.circularityIndex.toFixed(2)} / 1.0
                        </p>
                      </div>
                    </CardContent>
                  </Card>
                </TooltipTrigger>
                <TooltipContent>
                  <p>Measure of process circularity</p>
                </TooltipContent>
              </Tooltip>
            </TooltipProvider>

            <TooltipProvider>
              <Tooltip>
                <TooltipTrigger asChild>
                  <Card>
                    <CardContent className="pt-6">
                      <div className="text-center">
                        <p className="text-sm font-medium text-muted-foreground">
                          Resource Efficiency
                        </p>
                        <p className="text-2xl font-bold" style={{ color: getScoreColor(metrics.resourceEfficiency) }}>
                          {formatNumber(metrics.resourceEfficiency)}%
                        </p>
                      </div>
                    </CardContent>
                  </Card>
                </TooltipTrigger>
                <TooltipContent>
                  <p>Resource utilization efficiency</p>
                </TooltipContent>
              </Tooltip>
            </TooltipProvider>
          </div>

          <div className="flex items-center gap-2 text-sm">
            {metrics.sustainabilityScore >= 70 ? (
              <CheckCircle className="h-4 w-4 text-emerald-500" />
            ) : (
              <AlertCircle className="h-4 w-4 text-yellow-500" />
            )}
            <span className="text-muted-foreground">
              {metrics.sustainabilityScore >= 70
                ? 'Process meets sustainability targets'
                : metrics.sustainabilityScore >= 50
                ? 'Process needs minor improvements'
                : 'Significant improvements needed'}
            </span>
          </div>
        </div>
      </CardContent>
    </Card>
  );
} 