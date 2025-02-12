"use client";

import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { formatCurrency } from '@/lib/formatters';
import { DollarSign, TrendingUp, Clock, Percent } from 'lucide-react';

interface ProfitabilityMetricsProps {
  metrics: {
    npv: number;
    roi: number;
    payback_period: number;
    irr: number;
  };
}

export function ProfitabilityMetrics({ metrics }: ProfitabilityMetricsProps) {
  const profitabilityMetrics = [
    {
      label: "Net Present Value",
      value: metrics.npv,
      format: (value: number) => formatCurrency(value),
      icon: <DollarSign className="h-4 w-4" />,
      description: "Present value of future cash flows",
      threshold: 0,
      suffix: "",
    },
    {
      label: "Return on Investment",
      value: metrics.roi,
      format: (value: number) => `${value.toFixed(1)}%`,
      icon: <Percent className="h-4 w-4" />,
      description: "Percentage return on initial investment",
      threshold: 15,
      suffix: "%",
    },
    {
      label: "Payback Period",
      value: metrics.payback_period,
      format: (value: number) => `${value.toFixed(1)} years`,
      icon: <Clock className="h-4 w-4" />,
      description: "Time to recover initial investment",
      threshold: 5,
      suffix: " years",
    },
    {
      label: "Internal Rate of Return",
      value: metrics.irr,
      format: (value: number) => `${value.toFixed(1)}%`,
      icon: <TrendingUp className="h-4 w-4" />,
      description: "Project's rate of return",
      threshold: 20,
      suffix: "%",
    },
  ];

  const getMetricStatus = (metric: typeof profitabilityMetrics[0]) => {
    if (metric.label === "Net Present Value") {
      return metric.value > metric.threshold;
    }
    if (metric.label === "Payback Period") {
      return metric.value < metric.threshold;
    }
    return metric.value > metric.threshold;
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle>Profitability Analysis</CardTitle>
      </CardHeader>
      <CardContent className="space-y-6">
        {profitabilityMetrics.map((metric) => {
          const isPositive = getMetricStatus(metric);
          return (
            <div key={metric.label} className="space-y-2">
              <div className="flex items-center gap-2">
                <div className={`rounded-full p-2 ${
                  isPositive ? 'bg-emerald-100 text-emerald-700' : 'bg-yellow-100 text-yellow-700'
                }`}>
                  {metric.icon}
                </div>
                <div>
                  <p className="font-medium">{metric.label}</p>
                  <p className="text-sm text-muted-foreground">
                    {metric.description}
                  </p>
                </div>
                <div className="ml-auto text-right">
                  <p className={`text-lg font-semibold ${
                    isPositive ? 'text-emerald-600' : 'text-yellow-600'
                  }`}>
                    {metric.format(metric.value)}
                  </p>
                </div>
              </div>
              {metric.label !== "Net Present Value" && (
                <Progress
                  value={metric.label === "Payback Period"
                    ? Math.max(0, 100 - (metric.value / metric.threshold) * 100)
                    : (metric.value / metric.threshold) * 100}
                  className="h-2"
                />
              )}
            </div>
          );
        })}
      </CardContent>
    </Card>
  );
} 