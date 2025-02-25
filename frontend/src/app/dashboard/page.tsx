"use client";

import React from 'react';
import DashboardLayout from '@/components/layout/DashboardLayout';
import { Card, CardContent } from "@/components/ui/card";
import { 
  Activity, 
  DollarSign, 
  Leaf,
  Plus,
  CircleDollarSign,
  TrendingUp,
  LineChart,
  BarChart3,
  Droplets,
  Wind,
  Scale,
  Timer,
  Target,
  Package,
  Zap,
  LucideIcon,
  ArrowRight
} from 'lucide-react';
import { Button } from "@/components/ui/button";
import Link from 'next/link';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { MotionDiv } from "@/components/motion";
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip";

interface AnalysisFeature {
  icon: LucideIcon;
  label: string;
  color: string;
}

interface AnalysisType {
  title: string;
  description: string;
  href: string;
  features: AnalysisFeature[];
  bgGradient: string;
  accentColor: string;
  borderColor: string;
}

export default function DashboardPage() {
  const analysisTypes: AnalysisType[] = [
    {
      title: "Economic Analysis",
      description: "Comprehensive cost and profitability analysis",
      href: "/dashboard/economic_analysis",
      features: [
        { icon: CircleDollarSign, label: "Cost Breakdown", color: "text-green-500" },
        { icon: TrendingUp, label: "Profitability Metrics", color: "text-green-600" },
        { icon: LineChart, label: "Sensitivity Analysis", color: "text-green-700" }
      ],
      bgGradient: "from-green-500/5 via-background to-background",
      accentColor: "text-green-500",
      borderColor: "group-hover:border-green-500/50"
    },
    {
      title: "Technical Analysis",
      description: "Process efficiency and performance metrics",
      href: "/dashboard/technical_analysis",
      features: [
        { icon: Target, label: "Process Efficiency", color: "text-blue-500" },
        { icon: Activity, label: "Performance Monitoring", color: "text-blue-600" },
        { icon: Package, label: "Resource Optimization", color: "text-blue-700" }
      ],
      bgGradient: "from-blue-500/5 via-background to-background",
      accentColor: "text-blue-500",
      borderColor: "group-hover:border-blue-500/50"
    },
    {
      title: "Environmental Analysis",
      description: "Sustainability and environmental impact assessment",
      href: "/dashboard/environmental_analysis",
      features: [
        { icon: Droplets, label: "Water Impact Analysis", color: "text-emerald-500" },
        { icon: Wind, label: "Carbon Footprint", color: "text-emerald-600" },
        { icon: Scale, label: "Resource Efficiency", color: "text-emerald-700" }
      ],
      bgGradient: "from-emerald-500/5 via-background to-background",
      accentColor: "text-emerald-500",
      borderColor: "group-hover:border-emerald-500/50"
    }
  ];

  return (
    <DashboardLayout>
      <div className="flex flex-col gap-8">
        {/* Header */}
        <MotionDiv
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="flex flex-col sm:flex-row sm:items-center justify-between gap-4"
        >
          <div className="space-y-1">
            <h1 className="text-3xl font-bold tracking-tight bg-gradient-to-r from-foreground to-foreground/70 bg-clip-text text-transparent">
              Dashboard
            </h1>
            <p className="text-muted-foreground max-w-[500px]">
              Overview of your process analysis activities
            </p>
          </div>
          <DropdownMenu>
            <TooltipProvider>
              <Tooltip>
                <TooltipTrigger asChild>
                  <DropdownMenuTrigger asChild>
                    <Button className="gap-2 relative overflow-hidden group">
                      <Plus className="h-4 w-4 transition-transform group-hover:rotate-90 duration-200" />
                      New Analysis
                      <MotionDiv
                        className="absolute inset-0 bg-primary/10"
                        initial={{ scale: 0, opacity: 0 }}
                        whileHover={{ scale: 1, opacity: 1 }}
                        transition={{ duration: 0.2 }}
                      />
                    </Button>
                  </DropdownMenuTrigger>
                </TooltipTrigger>
                <TooltipContent>
                  <p>Start a new analysis</p>
                </TooltipContent>
              </Tooltip>
            </TooltipProvider>
            <DropdownMenuContent align="end" className="w-48">
              {analysisTypes.map((type) => {
                const Icon = type.features[0].icon;
                return (
                  <DropdownMenuItem key={type.title} asChild>
                    <Link href={type.href} className="flex items-center gap-2 cursor-pointer">
                      <Icon className={`h-4 w-4 ${type.accentColor}`} />
                      <span>{type.title}</span>
                    </Link>
                  </DropdownMenuItem>
                );
              })}
            </DropdownMenuContent>
          </DropdownMenu>
        </MotionDiv>

        {/* Analysis Types Grid */}
        <div className="grid gap-6 md:grid-cols-3">
          {analysisTypes.map((analysis, index) => {
            const MainIcon = analysis.features[0].icon;
            return (
              <MotionDiv
                key={analysis.title}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: index * 0.1 }}
              >
                <Link 
                  href={analysis.href}
                  className="group block"
                >
                  <Card className={`
                    relative h-full transition-all duration-300 
                    hover:shadow-lg hover:-translate-y-1
                    bg-gradient-to-br ${analysis.bgGradient}
                    border ${analysis.borderColor}
                    overflow-hidden
                  `}>
                    <CardContent className="p-6 space-y-4">
                      <div className="space-y-2">
                        <div className="flex items-center gap-2">
                          <MotionDiv
                            whileHover={{ rotate: 5, scale: 1.1 }}
                            transition={{ type: "spring", stiffness: 400, damping: 10 }}
                            className={`p-2 rounded-lg bg-gradient-to-br from-${analysis.accentColor}/20 to-${analysis.accentColor}/10`}
                          >
                            <MainIcon className={`h-6 w-6 ${analysis.accentColor}`} />
                          </MotionDiv>
                          <div className="flex items-center gap-2">
                            <h3 className="text-xl font-semibold">{analysis.title}</h3>
                            <ArrowRight className={`h-4 w-4 opacity-0 -translate-x-2 transition-all duration-200 ${analysis.accentColor} group-hover:opacity-100 group-hover:translate-x-0`} />
                          </div>
                        </div>
                        <p className="text-sm text-muted-foreground">
                          {analysis.description}
                        </p>
                      </div>

                      <div className="space-y-2 pt-2">
                        {analysis.features.map((feature, featureIndex) => {
                          const FeatureIcon = feature.icon;
                          return (
                            <MotionDiv 
                              key={feature.label}
                              className={`
                                flex items-center gap-2 text-sm
                                animate-in fade-in slide-in-from-bottom-2
                              `}
                              style={{ animationDelay: `${featureIndex * 150}ms` }}
                              whileHover={{ x: 4 }}
                              transition={{ duration: 0.2 }}
                            >
                              <FeatureIcon className={`h-4 w-4 ${feature.color}`} />
                              <span>{feature.label}</span>
                            </MotionDiv>
                          );
                        })}
                      </div>
                    </CardContent>
                  </Card>
                </Link>
              </MotionDiv>
            );
          })}
        </div>
      </div>
    </DashboardLayout>
  );
} 