"use client";

import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { ParticleMetrics } from '@/types/technical';
import { motion } from 'framer-motion';
import { BarChart3, Ruler, Droplets, Calculator, Maximize2 } from 'lucide-react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from 'recharts';

export interface ParticleSizeDisplayProps {
  metrics: ParticleMetrics;
}

export function ParticleSizeDisplay({ metrics }: ParticleSizeDisplayProps) {
  const sizeData = [
    {
      name: 'D10',
      value: metrics.d10,
      quality: metrics.D10,
      label: '10th Percentile',
    },
    {
      name: 'D50',
      value: metrics.d50,
      quality: metrics.D50,
      label: 'Median Size',
    },
    {
      name: 'D90',
      value: metrics.d90,
      quality: metrics.D90,
      label: '90th Percentile',
    },
  ];

  const statisticalMetrics = [
    {
      label: "Mean Size",
      value: metrics.mean,
      unit: "μm",
      color: "text-blue-500"
    },
    {
      label: "Standard Deviation",
      value: metrics.std_dev,
      unit: "μm",
      color: "text-indigo-500"
    },
    {
      label: "Coefficient of Variation",
      value: metrics.cv,
      unit: "%",
      color: "text-purple-500"
    },
    {
      label: "Distribution Span",
      value: metrics.span,
      quality: metrics.span,
      unit: "",
      color: "text-violet-500"
    }
  ];

  const surfaceMetrics = [
    {
      label: "Specific Surface Area",
      value: metrics.specific_surface_area,
      unit: "m²/g",
      color: "text-emerald-500"
    },
    {
      label: "Total Surface Area",
      value: metrics.total_surface_area,
      unit: "m²",
      color: "text-green-500"
    },
    {
      label: "Mean Surface Area",
      value: metrics.mean_surface_area,
      unit: "m²",
      color: "text-teal-500"
    }
  ];

  const moistureMetrics = [
    {
      label: "Pre-treatment Moisture",
      value: metrics.pre_treatment_moisture,
      unit: "%",
      color: "text-cyan-500"
    },
    {
      label: "Post-treatment Moisture",
      value: metrics.post_treatment_moisture,
      unit: "%",
      color: "text-sky-500"
    },
    {
      label: "Processing Moisture",
      value: metrics.processing_moisture,
      unit: "%",
      color: "text-blue-500"
    },
    {
      label: "Current Moisture",
      value: metrics.current_moisture,
      unit: "%",
      color: "text-indigo-500"
    }
  ];

  return (
    <div className="space-y-6">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <Card className="border-none shadow-lg bg-gradient-to-br from-blue-50 to-indigo-50 dark:from-blue-950/30 dark:to-indigo-950/30">
          <CardHeader>
            <div className="flex items-center space-x-2">
              <BarChart3 className="h-5 w-5 text-blue-500" />
              <CardTitle>Particle Size Distribution</CardTitle>
            </div>
          </CardHeader>
          <CardContent>
            <div className="h-[300px]">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={sizeData} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
                  <CartesianGrid strokeDasharray="3 3" className="opacity-50" />
                  <XAxis dataKey="name" />
                  <YAxis label={{ value: 'Size (μm)', angle: -90, position: 'insideLeft' }} />
                  <Tooltip
                    content={({ active, payload }) => {
                      if (active && payload && payload.length) {
                        const data = payload[0].payload;
                        return (
                          <div className="rounded-lg bg-white/90 dark:bg-gray-800/90 p-3 shadow-lg border backdrop-blur-sm">
                            <p className="font-medium text-blue-600 dark:text-blue-400">{data.label}</p>
                            <p className="text-sm text-gray-600 dark:text-gray-300">
                              Size: {data.value.toFixed(2)} μm
                            </p>
                            <p className="text-sm text-gray-600 dark:text-gray-300">
                              Quality: {data.quality.toFixed(1)}%
                            </p>
                          </div>
                        );
                      }
                      return null;
                    }}
                  />
                  <Bar
                    dataKey="value"
                    fill="url(#gradient)"
                    radius={[6, 6, 0, 0]}
                  />
                  <defs>
                    <linearGradient id="gradient" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="0%" stopColor="#3b82f6" stopOpacity={0.8}/>
                      <stop offset="100%" stopColor="#60a5fa" stopOpacity={0.3}/>
                    </linearGradient>
                  </defs>
                </BarChart>
              </ResponsiveContainer>
            </div>
          </CardContent>
        </Card>
      </motion.div>

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.1 }}
      >
        <Card className="border-none shadow-lg bg-gradient-to-br from-purple-50 to-indigo-50 dark:from-purple-950/30 dark:to-indigo-950/30">
          <CardHeader>
            <div className="flex items-center space-x-2">
              <Calculator className="h-5 w-5 text-purple-500" />
              <CardTitle>Statistical Analysis</CardTitle>
            </div>
          </CardHeader>
          <CardContent>
            <div className="grid gap-4 sm:grid-cols-2">
              {statisticalMetrics.map((metric, index) => (
                <motion.div
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ duration: 0.3, delay: index * 0.1 }}
                  key={metric.label}
                  className="flex justify-between items-center p-4 rounded-lg bg-white/50 dark:bg-white/5"
                >
                  <div>
                    <p className="font-medium">{metric.label}</p>
                  </div>
                  <div className="text-right">
                    <p className={`text-lg font-semibold ${metric.color}`}>
                      {metric.value.toFixed(2)}{metric.unit}
                    </p>
                    {metric.quality && (
                      <p className="text-sm text-muted-foreground">
                        Quality: {metric.quality.toFixed(1)}%
                      </p>
                    )}
                  </div>
                </motion.div>
              ))}
            </div>
          </CardContent>
        </Card>
      </motion.div>

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.2 }}
      >
        <Card className="border-none shadow-lg bg-gradient-to-br from-emerald-50 to-teal-50 dark:from-emerald-950/30 dark:to-teal-950/30">
          <CardHeader>
            <div className="flex items-center space-x-2">
              <Maximize2 className="h-5 w-5 text-emerald-500" />
              <CardTitle>Surface Area Analysis</CardTitle>
            </div>
          </CardHeader>
          <CardContent>
            <div className="grid gap-4 sm:grid-cols-2">
              {surfaceMetrics.map((metric, index) => (
                <motion.div
                  initial={{ opacity: 0, scale: 0.95 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{ duration: 0.3, delay: index * 0.1 }}
                  key={metric.label}
                  className="flex justify-between items-center p-4 rounded-lg bg-white/50 dark:bg-white/5"
                >
                  <div>
                    <p className="font-medium">{metric.label}</p>
                  </div>
                  <p className={`text-lg font-semibold ${metric.color}`}>
                    {metric.value.toExponential(2)}{metric.unit}
                  </p>
                </motion.div>
              ))}
            </div>
          </CardContent>
        </Card>
      </motion.div>

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.3 }}
      >
        <Card className="border-none shadow-lg bg-gradient-to-br from-cyan-50 to-blue-50 dark:from-cyan-950/30 dark:to-blue-950/30">
          <CardHeader>
            <div className="flex items-center space-x-2">
              <Droplets className="h-5 w-5 text-cyan-500" />
              <CardTitle>Moisture Content Analysis</CardTitle>
            </div>
          </CardHeader>
          <CardContent>
            <div className="grid gap-4 sm:grid-cols-2">
              {moistureMetrics.map((metric, index) => (
                <motion.div
                  initial={{ opacity: 0, x: 20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ duration: 0.3, delay: index * 0.1 }}
                  key={metric.label}
                  className="flex justify-between items-center p-4 rounded-lg bg-white/50 dark:bg-white/5"
                >
                  <div>
                    <p className="font-medium">{metric.label}</p>
                  </div>
                  <p className={`text-lg font-semibold ${metric.color}`}>
                    {metric.value.toFixed(1)}{metric.unit}
                  </p>
                </motion.div>
              ))}
            </div>
          </CardContent>
        </Card>
      </motion.div>

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.4 }}
        className="mt-4 text-center bg-gradient-to-r from-blue-500 to-indigo-500 text-white p-4 rounded-lg shadow-lg"
      >
        <p className="text-xl font-bold">
          Overall Quality Score: {metrics.overall.toFixed(1)}%
        </p>
      </motion.div>
    </div>
  );
} 