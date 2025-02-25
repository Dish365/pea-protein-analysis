"use client";

import React from 'react';
import { ComprehensiveAnalysisResponse } from '@/types/economic';
import { CostBreakdown } from './CostBreakdown';
import { ProfitabilityMetrics } from './ProfitabilityMetrics';
import { SensitivityAnalysis } from './SensitivityAnalysis';
import { MotionDiv } from '@/components/motion';
import { Card } from '@/components/ui/card';
import { CircleDollarSign, TrendingUp, LineChart } from 'lucide-react';

interface EconomicAnalysisViewProps {
  data: ComprehensiveAnalysisResponse;
}

export const EconomicAnalysisView: React.FC<EconomicAnalysisViewProps> = ({ data }) => {
  const sections = [
    {
      component: <CostBreakdown data={data} />,
      icon: <CircleDollarSign className="w-6 h-6 text-blue-500" />,
      title: "Cost Analysis",
      description: "Detailed breakdown of capital and operational expenditures"
    },
    {
      component: <ProfitabilityMetrics data={data} />,
      icon: <TrendingUp className="w-6 h-6 text-emerald-500" />,
      title: "Profitability Metrics",
      description: "Key performance indicators and financial metrics"
    },
    {
      component: <SensitivityAnalysis data={data} />,
      icon: <LineChart className="w-6 h-6 text-purple-500" />,
      title: "Sensitivity Analysis",
      description: "Impact analysis of key variables on project outcomes"
    }
  ];

  return (
    <div className="space-y-8 max-w-7xl mx-auto">
      {sections.map((section, index) => (
        <MotionDiv
          key={section.title}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: index * 0.2 }}
        >
          <Card className="p-6 border-none shadow-lg bg-gradient-to-br from-background to-muted/20">
            <div className="mb-6">
              <div className="flex items-center gap-3">
                {section.icon}
                <div>
                  <h2 className="text-2xl font-bold">{section.title}</h2>
                  <p className="text-muted-foreground">{section.description}</p>
                </div>
              </div>
            </div>
            <MotionDiv
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.3, delay: 0.2 + index * 0.2 }}
            >
              {section.component}
            </MotionDiv>
          </Card>
        </MotionDiv>
      ))}
    </div>
  );
};
