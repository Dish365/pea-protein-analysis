"use client";

import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { SeparationMetrics } from '@/types/technical';
import { motion } from 'framer-motion';
import { Activity, Droplets, PieChart, Gauge, TrendingUp, ArrowUpRight, Layers } from 'lucide-react';

export interface EfficiencyMetricsProps {
  metrics: SeparationMetrics;
}

export function EfficiencyMetrics({ metrics }: EfficiencyMetricsProps) {
  const mainMetrics = [
    {
      label: "Separation Efficiency",
      value: metrics.separation_efficiency,
      description: "Overall separation process efficiency",
      unit: "%",
      icon: <Activity className="h-5 w-5" />,
      color: metrics.separation_efficiency > 50 ? "text-emerald-500" : "text-amber-500"
    },
    {
      label: "Protein Enrichment",
      value: metrics.protein_enrichment,
      description: "Protein concentration improvement",
      unit: "%",
      icon: <TrendingUp className="h-5 w-5" />,
      color: "text-blue-500"
    },
    {
      label: "Separation Factor",
      value: metrics.separation_factor,
      description: "Effectiveness of separation process",
      unit: "×",
      icon: <Layers className="h-5 w-5" />,
      color: "text-indigo-500"
    }
  ];

  const componentRecoveries = [
    {
      label: "Protein Recovery",
      value: metrics.component_recoveries.protein,
      description: "Protein fraction recovery",
      unit: "%",
      color: "text-amber-500"
    },
    {
      label: "Starch Recovery",
      value: metrics.component_recoveries.starch,
      description: "Starch fraction recovery",
      unit: "%",
      color: "text-blue-500"
    },
    {
      label: "Fiber Recovery",
      value: metrics.component_recoveries.fiber,
      description: "Fiber fraction recovery",
      unit: "%",
      color: "text-green-500"
    },
    {
      label: "Others Recovery",
      value: metrics.component_recoveries.others,
      description: "Other components recovery",
      unit: "%",
      color: "text-purple-500"
    }
  ];

  return (
    <Card className="border-none shadow-lg bg-gradient-to-br from-emerald-50 to-teal-50 dark:from-emerald-950/30 dark:to-teal-950/30">
      <CardHeader>
        <div className="flex items-center space-x-2">
          <Activity className="h-5 w-5 text-emerald-500" />
          <CardTitle>Main Efficiency Metrics</CardTitle>
        </div>
      </CardHeader>
      <CardContent className="space-y-6">
        {/* Main Metrics */}
        <div className="space-y-4">
          {mainMetrics.map((metric, index) => (
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.3, delay: index * 0.1 }}
              key={metric.label}
              className="bg-white/50 dark:bg-white/5 rounded-lg p-4 space-y-2"
            >
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-2">
                  <span className={metric.color}>{metric.icon}</span>
                  <div>
                    <p className="font-medium">{metric.label}</p>
                    <p className="text-sm text-muted-foreground">
                      {metric.description}
                    </p>
                  </div>
                </div>
                <span className={`text-lg font-semibold ${metric.color}`}>
                  {metric.value.toFixed(2)}{metric.unit}
                </span>
              </div>
              {metric.unit === "%" && (
                <Progress 
                  value={metric.value} 
                  className="h-2 bg-emerald-100 dark:bg-emerald-900"
                  indicatorClassName={`bg-gradient-to-r ${
                    metric.value > 50 
                      ? "from-emerald-500 to-green-500"
                      : "from-amber-500 to-orange-500"
                  }`}
                />
              )}
            </motion.div>
          ))}
        </div>

        {/* Component Recovery Distribution */}
        <div className="space-y-4">
          <div className="flex items-center space-x-2">
            <PieChart className="h-5 w-5 text-emerald-500" />
            <h3 className="font-semibold">Component Recovery Distribution</h3>
          </div>
          <div className="space-y-3">
            {componentRecoveries.map((metric, index) => (
              <motion.div
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.3, delay: 0.3 + index * 0.1 }}
                key={metric.label}
                className="space-y-2"
              >
                <div className="flex justify-between items-center">
                  <p className="text-sm font-medium">{metric.label}</p>
                  <span className={`text-sm font-semibold ${metric.color}`}>
                    {metric.value.toFixed(2)}%
                  </span>
                </div>
                <Progress 
                  value={metric.value} 
                  className="h-1.5 bg-emerald-100 dark:bg-emerald-900"
                  indicatorClassName={`bg-gradient-to-r ${
                    metric.label.includes("Protein") 
                      ? "from-amber-500 to-yellow-500"
                      : metric.label.includes("Starch")
                      ? "from-blue-500 to-cyan-500"
                      : metric.label.includes("Fiber")
                      ? "from-green-500 to-emerald-500"
                      : "from-purple-500 to-pink-500"
                  }`}
                />
              </motion.div>
            ))}
          </div>
        </div>
      </CardContent>
    </Card>
  );
} 