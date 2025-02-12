"use client";

import React from 'react';
import { DollarSign, Percent, Clock, TrendingUp } from 'lucide-react';
import { formatCurrency } from '@/lib/formatters';
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

interface ProfitabilityMetricsProps {
  metrics: {
    npv: number;
    roi: number;
    paybackPeriod: number;
    irr: number;
  };
  totalInvestment: number;
  annualCosts: number;
}

export function ProfitabilityMetrics({ 
  metrics,
  totalInvestment,
  annualCosts
}: ProfitabilityMetricsProps) {
  const getMetricStatus = (value: number, thresholds: { low: number; medium: number }, inverse = false) => {
    const effectiveValue = inverse ? -value : value;
    const effectiveThresholds = inverse ? 
      { low: -thresholds.medium, medium: -thresholds.low } :
      thresholds;

    if (effectiveValue >= effectiveThresholds.medium) {
      return { 
        color: 'text-emerald-600',
        bgColor: 'bg-emerald-100',
        textColor: 'text-emerald-700',
        variant: 'success' as const
      };
    }
    if (effectiveValue >= effectiveThresholds.low) {
      return { 
        color: 'text-yellow-600',
        bgColor: 'bg-yellow-100',
        textColor: 'text-yellow-700',
        variant: 'warning' as const
      };
    }
    return { 
      color: 'text-destructive',
      bgColor: 'bg-red-100',
      textColor: 'text-red-700',
      variant: 'destructive' as const
    };
  };

  const metrics_config = [
    {
      title: 'Net Present Value',
      value: metrics.npv,
      icon: <DollarSign className="h-4 w-4" />,
      formatter: (value: number) => formatCurrency(value),
      tooltip: 'Present value of future cash flows minus initial investment',
      thresholds: { low: 0, medium: totalInvestment * 0.2 }
    },
    {
      title: 'Return on Investment',
      value: metrics.roi,
      icon: <Percent className="h-4 w-4" />,
      suffix: '%',
      formatter: (value: number) => value.toFixed(1),
      tooltip: 'Percentage return on initial investment',
      thresholds: { low: 15, medium: 25 }
    },
    {
      title: 'Internal Rate of Return',
      value: metrics.irr,
      icon: <TrendingUp className="h-4 w-4" />,
      suffix: '%',
      formatter: (value: number) => value.toFixed(1),
      tooltip: 'Discount rate that makes NPV zero',
      thresholds: { low: 10, medium: 20 }
    },
    {
      title: 'Payback Period',
      value: metrics.paybackPeriod,
      icon: <Clock className="h-4 w-4" />,
      suffix: 'years',
      formatter: (value: number) => value.toFixed(1),
      tooltip: 'Time required to recover the investment',
      thresholds: { low: 5, medium: 3 },
      inverse: true
    }
  ];

  return (
    <Card>
      <CardHeader>
        <CardTitle>Profitability Analysis</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="grid gap-4 sm:grid-cols-2">
          {metrics_config.map((metric, index) => {
            const status = getMetricStatus(metric.value, metric.thresholds, metric.inverse);
            const progressValue = metric.inverse ?
              Math.max(0, 100 - (metric.value / metric.thresholds.low) * 100) :
              Math.min(100, (metric.value / metric.thresholds.medium) * 100);

            return (
              <TooltipProvider key={index}>
                <Tooltip>
                  <TooltipTrigger asChild>
                    <Card>
                      <CardContent className="pt-6">
                        <div className="flex items-center gap-2">
                          <div className={`rounded-full p-2 ${status.bgColor}`}>
                            {metric.icon}
                          </div>
                          <div className="flex-1">
                            <p className="text-sm font-medium text-muted-foreground">
                              {metric.title}
                            </p>
                            <div className="flex items-center gap-2">
                              <p className={`text-2xl font-bold ${status.color}`}>
                                {metric.formatter(metric.value)}
                              </p>
                              {metric.suffix && (
                                <span className={`text-sm ${status.color}`}>
                                  {metric.suffix}
                                </span>
                              )}
                            </div>
                          </div>
                          <Badge variant={status.variant}>
                            {status.variant === 'success' ? 'Good' :
                             status.variant === 'warning' ? 'Fair' : 'Poor'}
                          </Badge>
                        </div>
                        <div className="mt-4">
                          <Progress
                            value={progressValue}
                            className={status.bgColor}
                            indicatorColor={
                              status.variant === 'success' ? 'rgb(16 185 129)' :  // emerald-500
                              status.variant === 'warning' ? 'rgb(234 179 8)' :   // yellow-500
                              'rgb(239 68 68)'  // red-500
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
            );
          })}
        </div>
      </CardContent>
    </Card>
  );
} 