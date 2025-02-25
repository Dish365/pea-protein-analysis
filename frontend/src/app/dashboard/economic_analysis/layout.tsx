"use client";

import React from 'react';
import { CircleDollarSign, TrendingUp, Calculator, PieChart, ArrowUpRight } from 'lucide-react';
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip";
import { MotionDiv, fadeIn, slideUp } from "@/components/motion";

export default function AnalysisLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="relative min-h-screen overflow-hidden">
      {/* Background Patterns */}
      <div className="absolute inset-0 bg-grid-black/[0.02] -z-10" />
      <div className="absolute inset-0 bg-gradient-to-br from-blue-50/50 via-background to-emerald-50/50 dark:from-blue-950/20 dark:via-background dark:to-emerald-950/20 -z-10" />
      <div className="absolute inset-0 bg-noise opacity-20 -z-10" />
      
      {/* Animated Background Elements */}
      <MotionDiv
        className="absolute -top-40 -right-40 w-80 h-80 bg-primary/10 rounded-full blur-3xl"
        animate={{
          scale: [1, 1.2, 1],
          opacity: [0.3, 0.2, 0.3],
        }}
        transition={{
          duration: 8,
          repeat: Infinity,
          ease: "easeInOut"
        }}
      />
      <MotionDiv
        className="absolute -bottom-40 -left-40 w-80 h-80 bg-blue-500/10 rounded-full blur-3xl"
        animate={{
          scale: [1.2, 1, 1.2],
          opacity: [0.2, 0.3, 0.2],
        }}
        transition={{
          duration: 8,
          repeat: Infinity,
          ease: "easeInOut",
          delay: 2
        }}
      />
      
      {/* Header Section */}
      <div className="border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
        <MotionDiv 
          {...slideUp}
          transition={{ duration: 0.5 }}
          className="container flex flex-col gap-4 py-6"
        >
          <div className="flex items-center gap-3">
            <MotionDiv
              whileHover={{ scale: 1.05, rotate: 5 }}
              whileTap={{ scale: 0.95 }}
              className="p-2 rounded-lg bg-gradient-to-br from-primary/20 to-primary/10"
            >
              <CircleDollarSign className="w-8 h-8 text-primary" />
            </MotionDiv>
            <div>
              <h1 className="text-3xl font-bold tracking-tight bg-gradient-to-r from-primary to-blue-600 bg-clip-text text-transparent">
                Economic Analysis
              </h1>
              <p className="text-muted-foreground">
                Comprehensive financial assessment and profitability analysis
              </p>
            </div>
          </div>
          
          <div className="flex flex-wrap gap-4 text-sm">
            <TooltipProvider>
              <Tooltip>
                <TooltipTrigger asChild>
                  <MotionDiv
                    whileHover={{ scale: 1.02 }}
                    className="flex items-center gap-2 px-3 py-1.5 rounded-full bg-emerald-50 dark:bg-emerald-950/30 text-emerald-600 dark:text-emerald-400 border border-emerald-100 dark:border-emerald-900"
                  >
                    <TrendingUp className="w-4 h-4" />
                    <span>Profitability Metrics</span>
                    <ArrowUpRight className="w-3 h-3 ml-1" />
                  </MotionDiv>
                </TooltipTrigger>
                <TooltipContent>
                  <p>Analyze key financial performance indicators</p>
                </TooltipContent>
              </Tooltip>

              <Tooltip>
                <TooltipTrigger asChild>
                  <MotionDiv
                    whileHover={{ scale: 1.02 }}
                    className="flex items-center gap-2 px-3 py-1.5 rounded-full bg-blue-50 dark:bg-blue-950/30 text-blue-600 dark:text-blue-400 border border-blue-100 dark:border-blue-900"
                  >
                    <Calculator className="w-4 h-4" />
                    <span>Sensitivity Analysis</span>
                    <ArrowUpRight className="w-3 h-3 ml-1" />
                  </MotionDiv>
                </TooltipTrigger>
                <TooltipContent>
                  <p>Evaluate impact of variable changes on outcomes</p>
                </TooltipContent>
              </Tooltip>

              <Tooltip>
                <TooltipTrigger asChild>
                  <MotionDiv
                    whileHover={{ scale: 1.02 }}
                    className="flex items-center gap-2 px-3 py-1.5 rounded-full bg-purple-50 dark:bg-purple-950/30 text-purple-600 dark:text-purple-400 border border-purple-100 dark:border-purple-900"
                  >
                    <PieChart className="w-4 h-4" />
                    <span>Cost Structure</span>
                    <ArrowUpRight className="w-3 h-3 ml-1" />
                  </MotionDiv>
                </TooltipTrigger>
                <TooltipContent>
                  <p>Detailed breakdown of costs and investments</p>
                </TooltipContent>
              </Tooltip>
            </TooltipProvider>
          </div>
        </MotionDiv>
      </div>

      {/* Main Content */}
      <MotionDiv
        {...fadeIn}
        transition={{ duration: 0.5, delay: 0.2 }}
        className="container py-8"
      >
        <div className="rounded-xl border bg-background/60 backdrop-blur-sm shadow-sm">
          <div className="p-6">
            {children}
          </div>
        </div>
      </MotionDiv>
    </div>
  );
}
