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
  LucideIcon
} from 'lucide-react';
import { Button } from "@/components/ui/button";
import Link from 'next/link';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";

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
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold tracking-tight">Dashboard</h1>
            <p className="text-muted-foreground">
              Overview of your process analysis activities
            </p>
          </div>
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button className="gap-2">
                <Plus className="h-4 w-4" />
                New Analysis
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end" className="w-48">
              {analysisTypes.map((type) => {
                const Icon = type.features[0].icon;
                return (
                  <DropdownMenuItem key={type.title} asChild>
                    <Link href={type.href} className="flex items-center gap-2">
                      <Icon className={`h-4 w-4 ${type.accentColor}`} />
                      <span>{type.title}</span>
                    </Link>
                  </DropdownMenuItem>
                );
              })}
            </DropdownMenuContent>
          </DropdownMenu>
        </div>

        {/* Analysis Types Grid */}
        <div className="grid gap-6 md:grid-cols-3">
          {analysisTypes.map((analysis) => {
            const MainIcon = analysis.features[0].icon;
            return (
              <Link 
                key={analysis.title} 
                href={analysis.href}
                className="group"
              >
                <Card className={`
                  h-full transition-all duration-300 
                  hover:shadow-lg hover:scale-[1.02]
                  bg-gradient-to-br ${analysis.bgGradient}
                  border ${analysis.borderColor}
                `}>
                  <CardContent className="p-6 space-y-4">
                    <div className="space-y-2">
                      <div className="flex items-center gap-2">
                        <MainIcon className={`h-6 w-6 ${analysis.accentColor}`} />
                        <h3 className="text-xl font-semibold">{analysis.title}</h3>
                      </div>
                      <p className="text-sm text-muted-foreground">
                        {analysis.description}
                      </p>
                    </div>

                    <div className="space-y-2 pt-2">
                      {analysis.features.map((feature, index) => {
                        const FeatureIcon = feature.icon;
                        return (
                          <div 
                            key={feature.label}
                            className={`
                              flex items-center gap-2 text-sm
                              animate-in fade-in slide-in-from-bottom-2
                            `}
                            style={{ animationDelay: `${index * 150}ms` }}
                          >
                            <FeatureIcon className={`h-4 w-4 ${feature.color}`} />
                            <span>{feature.label}</span>
                          </div>
                        );
                      })}
                    </div>
                  </CardContent>
                </Card>
              </Link>
            );
          })}
        </div>
      </div>
    </DashboardLayout>
  );
} 