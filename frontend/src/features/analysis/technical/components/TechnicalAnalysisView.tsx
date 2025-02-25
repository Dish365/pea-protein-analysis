"use client";

import React from 'react';
import { AlertCircle, Loader2, TrendingUp, Droplets, PieChart, BarChart3, Gauge, ArrowUpRight } from 'lucide-react';
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { TechnicalResults } from '@/types/technical';
import { EfficiencyMetrics } from './EfficiencyMetrics';
import { ProteinRecoveryCard } from './ProteinRecoveryCard';
import { ParticleSizeDisplay } from './ParticleSizeDisplay';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Skeleton } from '@/components/ui/skeleton';
import { Progress } from '@/components/ui/progress';
import { motion } from 'framer-motion';
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from "@/components/ui/tooltip";

interface TechnicalAnalysisViewProps {
  data?: TechnicalResults;
  isLoading?: boolean;
  error?: string;
}

export function TechnicalAnalysisView({ 
  data, 
  isLoading, 
  error 
}: TechnicalAnalysisViewProps) {
  if (isLoading) {
    return (
      <div className="space-y-6">
        <Card className="p-6">
          <div className="flex items-center space-x-4">
            <Loader2 className="h-4 w-4 animate-spin" />
            <div className="space-y-2">
              <Skeleton className="h-4 w-[200px]" />
              <Skeleton className="h-4 w-[150px]" />
            </div>
          </div>
        </Card>
      </div>
    );
  }

  if (error) {
    return (
      <Alert variant="destructive">
        <AlertCircle className="h-4 w-4" />
        <AlertTitle>Error</AlertTitle>
        <AlertDescription>
          {error}
          <button 
            onClick={() => window.location.reload()}
            className="underline ml-2 hover:text-muted-foreground"
          >
            Try reloading
          </button>
        </AlertDescription>
      </Alert>
    );
  }

  if (!data) {
    return (
      <Alert>
        <AlertCircle className="h-4 w-4" />
        <AlertTitle>No Data</AlertTitle>
        <AlertDescription>
          No technical analysis data available. Please ensure all required parameters are provided.
        </AlertDescription>
      </Alert>
    );
  }

  const { 
    recovery_metrics,
    separation_metrics,
    particle_metrics,
    process_performance
  } = data;

  const hasValidData = recovery_metrics && 
    separation_metrics && 
    particle_metrics &&
    typeof recovery_metrics.recovery_rate === 'number' &&
    typeof separation_metrics.separation_efficiency === 'number' &&
    typeof particle_metrics.d10 === 'number';

  if (!hasValidData) {
    return (
      <Alert>
        <AlertCircle className="h-4 w-4" />
        <AlertTitle>Invalid Data</AlertTitle>
        <AlertDescription>
          The technical analysis data is incomplete or invalid. Please check the input parameters.
        </AlertDescription>
      </Alert>
    );
  }

  return (
    <motion.div 
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.5 }}
      className="space-y-8 max-w-7xl mx-auto px-4"
    >
      {/* Main Analysis Cards */}
      <div className="grid gap-6 md:grid-cols-2">
        <motion.div
          initial={{ y: 20 }}
          animate={{ y: 0 }}
          transition={{ duration: 0.5 }}
        >
          <ProteinRecoveryCard recovery={recovery_metrics} />
        </motion.div>

        <motion.div
          initial={{ y: 20 }}
          animate={{ y: 0 }}
          transition={{ duration: 0.5, delay: 0.1 }}
        >
          <EfficiencyMetrics metrics={separation_metrics} />
        </motion.div>
      </div>

      {/* Process Performance Card */}
      {process_performance && (
        <motion.div
          initial={{ y: 20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ duration: 0.5, delay: 0.2 }}
        >
          <Card className="border-none shadow-lg bg-gradient-to-br from-green-50 to-emerald-50 dark:from-green-950/30 dark:to-emerald-950/30">
            <CardHeader>
              <div className="flex items-center space-x-2">
                <Gauge className="h-5 w-5 text-green-500" />
                <CardTitle>Overall Process Performance</CardTitle>
              </div>
            </CardHeader>
            <CardContent>
              <div className="grid gap-6 sm:grid-cols-3">
                <motion.div
                  initial={{ scale: 0.9, opacity: 0 }}
                  animate={{ scale: 1, opacity: 1 }}
                  transition={{ duration: 0.3 }}
                  className="space-y-2"
                >
                  <TooltipProvider>
                    <Tooltip>
                      <TooltipTrigger asChild>
                        <p className="text-sm text-green-600 dark:text-green-300 cursor-help">
                          Cumulative Efficiency
                        </p>
                      </TooltipTrigger>
                      <TooltipContent className="max-w-[250px]">
                        <p>Overall efficiency of the entire process, considering all steps and their combined impact on protein extraction.</p>
                      </TooltipContent>
                    </Tooltip>
                  </TooltipProvider>
                  <p className="text-3xl font-bold text-green-900 dark:text-green-100">
                    {process_performance.cumulative_efficiency.toFixed(1)}%
                  </p>
                  <Progress 
                    value={process_performance.cumulative_efficiency} 
                    className="h-2 bg-green-100 dark:bg-green-900"
                    indicatorClassName="bg-gradient-to-r from-green-500 to-emerald-500" 
                  />
                </motion.div>
                <motion.div
                  initial={{ scale: 0.9, opacity: 0 }}
                  animate={{ scale: 1, opacity: 1 }}
                  transition={{ duration: 0.3, delay: 0.1 }}
                  className="space-y-2"
                >
                  <TooltipProvider>
                    <Tooltip>
                      <TooltipTrigger asChild>
                        <p className="text-sm text-green-600 dark:text-green-300 cursor-help">
                          Average Step Efficiency
                        </p>
                      </TooltipTrigger>
                      <TooltipContent className="max-w-[250px]">
                        <p>Mean efficiency across individual process steps, indicating the typical performance level of each separation stage.</p>
                      </TooltipContent>
                    </Tooltip>
                  </TooltipProvider>
                  <p className="text-3xl font-bold text-green-900 dark:text-green-100">
                    {process_performance.average_step_efficiency.toFixed(1)}%
                  </p>
                  <Progress 
                    value={process_performance.average_step_efficiency} 
                    className="h-2 bg-green-100 dark:bg-green-900"
                    indicatorClassName="bg-gradient-to-r from-green-500 to-emerald-500" 
                  />
                </motion.div>
                <motion.div
                  initial={{ scale: 0.9, opacity: 0 }}
                  animate={{ scale: 1, opacity: 1 }}
                  transition={{ duration: 0.3, delay: 0.2 }}
                  className="space-y-2"
                >
                  <TooltipProvider>
                    <Tooltip>
                      <TooltipTrigger asChild>
                        <p className="text-sm text-green-600 dark:text-green-300 cursor-help">
                          Purity Achievement
                        </p>
                      </TooltipTrigger>
                      <TooltipContent className="max-w-[250px]">
                        <p>Percentage of target purity achieved in the final product. 100% means the exact target protein concentration was reached.</p>
                      </TooltipContent>
                    </Tooltip>
                  </TooltipProvider>
                  <p className="text-3xl font-bold text-green-900 dark:text-green-100">
                    {process_performance.purity_achievement.toFixed(1)}%
                  </p>
                  <Progress 
                    value={process_performance.purity_achievement} 
                    className="h-2 bg-green-100 dark:bg-green-900"
                    indicatorClassName="bg-gradient-to-r from-green-500 to-emerald-500" 
                  />
                </motion.div>
              </div>
            </CardContent>
          </Card>
        </motion.div>
      )}

      {/* Particle Size Analysis */}
      <motion.div
        initial={{ y: 20, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ duration: 0.5, delay: 0.3 }}
      >
        <ParticleSizeDisplay metrics={particle_metrics} />
      </motion.div>
    </motion.div>
  );
}

export default TechnicalAnalysisView; 