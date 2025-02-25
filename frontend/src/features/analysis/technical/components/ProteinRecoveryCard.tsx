"use client";

import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { ProteinRecovery } from '@/types/technical';
import { ArrowUpRight, ArrowDownRight, Beaker, AlertTriangle } from 'lucide-react';
import { motion } from 'framer-motion';

export interface ProteinRecoveryCardProps {
  recovery: ProteinRecovery;
}

export function ProteinRecoveryCard({ recovery }: ProteinRecoveryCardProps) {
  const metrics = [
    {
      label: "Recovery Rate",
      value: recovery.recovery_rate,
      description: "Total protein recovery rate",
      unit: "%",
      icon: <ArrowUpRight className="h-5 w-5" />,
      color: recovery.recovery_rate > 50 ? "text-emerald-500" : "text-amber-500"
    },
    {
      label: "Process Efficiency",
      value: recovery.process_efficiency,
      description: "Overall process performance",
      unit: "%",
      icon: <Beaker className="h-5 w-5" />,
      color: recovery.process_efficiency > 50 ? "text-emerald-500" : "text-amber-500"
    },
    {
      label: "Protein Loss",
      value: recovery.protein_loss,
      description: "Total protein loss during process",
      unit: "kg",
      icon: <ArrowDownRight className="h-5 w-5" />,
      color: "text-red-500"
    },
    {
      label: "Concentration Factor",
      value: recovery.concentration_factor,
      description: "Protein concentration improvement",
      unit: "×",
      icon: <Beaker className="h-5 w-5" />,
      color: "text-blue-500"
    },
    {
      label: "Yield Gap",
      value: recovery.yield_gap,
      description: "Gap between actual and theoretical yield",
      unit: "%",
      icon: <AlertTriangle className="h-5 w-5" />,
      color: "text-red-500"
    },
    {
      label: "Improvement Potential",
      value: recovery.improvement_potential,
      description: "Potential for process improvement",
      unit: "%",
      icon: <ArrowUpRight className="h-5 w-5" />,
      color: "text-purple-500"
    },
    {
      label: "Moisture Compensation",
      value: recovery.moisture_compensation_factor,
      description: "Moisture impact on recovery",
      unit: "×",
      icon: <Beaker className="h-5 w-5" />,
      color: "text-blue-500"
    }
  ];

  return (
    <Card className="border-none shadow-lg">
      <CardHeader>
        <CardTitle className="text-xl font-bold">Protein Recovery Analysis</CardTitle>
      </CardHeader>
      <CardContent className="space-y-6">
        <div className="grid gap-6 sm:grid-cols-2">
          {metrics.map((metric, index) => (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
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
                  className={`h-2 ${
                    metric.label === "Yield Gap" || metric.label === "Improvement Potential"
                      ? "bg-red-100 dark:bg-red-900" 
                      : "bg-blue-100 dark:bg-blue-900"
                  }`}
                  indicatorClassName={
                    metric.label === "Yield Gap" || metric.label === "Improvement Potential"
                      ? "bg-gradient-to-r from-red-500 to-pink-500"
                      : metric.value > 50
                      ? "bg-gradient-to-r from-emerald-500 to-green-500"
                      : "bg-gradient-to-r from-amber-500 to-orange-500"
                  }
                />
              )}
            </motion.div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
} 