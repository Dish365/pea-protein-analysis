"use client";

import React from 'react';
import { Card, CardContent } from "@/components/ui/card";
import { Separator } from "@/components/ui/separator";
import { ComprehensiveAnalysisResponse } from '@/types/economic';
import { formatCurrency, formatPercentage } from '@/utils/formatters';
import { MotionDiv } from '@/components/motion';
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from "@/components/ui/tooltip";
import { 
  Building2, 
  CircleDollarSign, 
  BarChart3, 
  Wallet, 
  Clock, 
  Users, 
  Wrench, 
  Package, 
  Zap,
  TrendingUp,
  Info,
  DollarSign,
  Percent,
  ArrowUpRight,
  ArrowDownRight
} from 'lucide-react';
import { Progress } from "@/components/ui/progress";

interface CostBreakdownProps {
  data: ComprehensiveAnalysisResponse;
}

export const CostBreakdown: React.FC<CostBreakdownProps> = ({ data }) => {
  const { capex_analysis, opex_analysis } = data;
  
  if (!capex_analysis?.capex_summary || !opex_analysis?.opex_summary || !data.profitability_analysis?.metrics?.cost_structure) {
    return (
      <MotionDiv
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="bg-gradient-to-br from-background to-muted/20 rounded-lg p-6"
      >
        <div className="flex items-center gap-3 mb-4">
          <CircleDollarSign className="w-6 h-6 text-primary" />
          <h2 className="text-2xl font-bold">Cost Analysis</h2>
        </div>
        <p className="text-muted-foreground text-center">
          Cost breakdown data not available
        </p>
      </MotionDiv>
    );
  }

  const { capex_summary, working_capital_components, investment_efficiency } = capex_analysis;
  const { opex_summary } = opex_analysis;
  const { cost_structure } = data.profitability_analysis.metrics;

  const capitalExpenditures = [
    {
      title: "Equipment & Installation",
      value: capex_summary.total_capex,
      icon: <Building2 className="w-5 h-5" />,
      tooltip: "Total cost of equipment and installation",
      color: "text-blue-500"
    },
    {
      title: "Working Capital",
      value: capex_summary.working_capital,
      icon: <Wallet className="w-5 h-5" />,
      tooltip: "Current assets minus current liabilities needed for operations",
      color: "text-emerald-500"
    },
    {
      title: "Total Investment",
      value: capex_summary.total_investment,
      icon: <CircleDollarSign className="w-5 h-5" />,
      tooltip: "Total capital investment including working capital and contingency",
      color: "text-purple-500",
      highlight: true
    }
  ];

  const workingCapitalItems = [
    {
      title: "Inventory",
      value: working_capital_components.inventory.value,
      period: `${working_capital_components.inventory.months} months`,
      icon: <Package className="w-4 h-4" />,
      tooltip: "Value of inventory held for operations",
      color: "text-amber-500"
    },
    {
      title: "Accounts Receivable",
      value: working_capital_components.receivables.value,
      period: `${working_capital_components.receivables.days} days`,
      icon: <Clock className="w-4 h-4" />,
      tooltip: "Expected payments from customers",
      color: "text-blue-500"
    },
    {
      title: "Accounts Payable",
      value: working_capital_components.payables.value,
      period: `${working_capital_components.payables.days} days`,
      icon: <Clock className="w-4 h-4" />,
      tooltip: "Payments due to suppliers",
      color: "text-green-500"
    }
  ];

  const costCategories = [
    {
      title: "Fixed Costs",
      value: cost_structure.fixed_costs.value,
      percentage: cost_structure.fixed_costs.percentage,
      breakdown: [
        {
          label: "Labor",
          value: cost_structure.fixed_costs.breakdown.labor,
          icon: <Users className="w-4 h-4" />,
          color: "text-blue-500"
        },
        {
          label: "Maintenance",
          value: cost_structure.fixed_costs.breakdown.maintenance,
          icon: <Wrench className="w-4 h-4" />,
          color: "text-emerald-500"
        }
      ],
      icon: <DollarSign className="w-5 h-5" />,
      tooltip: "Costs that remain constant regardless of production volume",
      color: "text-indigo-500"
    },
    {
      title: "Variable Costs",
      value: cost_structure.variable_costs.value,
      percentage: cost_structure.variable_costs.percentage,
      breakdown: [
        {
          label: "Raw Materials",
          value: cost_structure.variable_costs.breakdown.raw_materials,
          icon: <Package className="w-4 h-4" />,
          color: "text-amber-500"
        },
        {
          label: "Utilities",
          value: cost_structure.variable_costs.breakdown.utilities,
          icon: <Zap className="w-4 h-4" />,
          color: "text-purple-500"
        }
      ],
      icon: <Percent className="w-5 h-5" />,
      tooltip: "Costs that vary with production volume",
      color: "text-violet-500"
    }
  ];

  return (
    <div className="space-y-6">
      {/* Capital Expenditure Overview */}
      <MotionDiv
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="grid grid-cols-1 md:grid-cols-3 gap-4"
      >
        {capitalExpenditures.map((item, index) => (
          <MotionDiv
            key={item.title}
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5, delay: index * 0.1 }}
            className={`bg-gradient-to-br from-card to-muted/20 rounded-lg p-4 shadow-lg ${
              item.highlight ? 'border-2 border-primary/20' : ''
            }`}
          >
            <TooltipProvider>
              <Tooltip>
                <TooltipTrigger asChild>
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <span className={item.color}>{item.icon}</span>
                      <h3 className="font-medium">{item.title}</h3>
                    </div>
                    <Info className="w-4 h-4 text-muted-foreground cursor-help" />
                  </div>
                </TooltipTrigger>
                <TooltipContent>
                  <p className="max-w-[250px]">{item.tooltip}</p>
                </TooltipContent>
              </Tooltip>
            </TooltipProvider>
            <p className="mt-2 text-2xl font-bold">{formatCurrency(item.value)}</p>
          </MotionDiv>
        ))}
      </MotionDiv>

      {/* Working Capital Components */}
      <MotionDiv
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.5, delay: 0.2 }}
        className="bg-gradient-to-br from-card to-muted/20 rounded-lg p-6 shadow-lg"
      >
        <div className="flex items-center gap-2 mb-4">
          <Wallet className="w-5 h-5 text-primary" />
          <h3 className="text-lg font-semibold">Working Capital Components</h3>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {workingCapitalItems.map((item, index) => (
            <MotionDiv
              key={item.title}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.3, delay: 0.3 + index * 0.1 }}
              className="bg-muted/30 rounded-lg p-4"
            >
              <TooltipProvider>
                <Tooltip>
                  <TooltipTrigger asChild>
                    <div className="flex items-center gap-2 mb-2">
                      <span className={item.color}>{item.icon}</span>
                      <div>
                        <p className="font-medium">{item.title}</p>
                        <p className="text-sm text-muted-foreground">{item.period}</p>
                      </div>
                    </div>
                  </TooltipTrigger>
                  <TooltipContent>
                    <p className="max-w-[250px]">{item.tooltip}</p>
                  </TooltipContent>
                </Tooltip>
              </TooltipProvider>
              <p className="text-xl font-bold">{formatCurrency(item.value)}</p>
            </MotionDiv>
          ))}
        </div>
      </MotionDiv>

      {/* Cost Structure */}
      <MotionDiv
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.5, delay: 0.3 }}
        className="grid grid-cols-1 md:grid-cols-2 gap-6"
      >
        {costCategories.map((category, index) => (
          <MotionDiv
            key={category.title}
            initial={{ opacity: 0, x: index === 0 ? -20 : 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5, delay: 0.4 + index * 0.1 }}
            className="bg-gradient-to-br from-card to-muted/20 rounded-lg p-6 shadow-lg"
          >
            <TooltipProvider>
              <Tooltip>
                <TooltipTrigger asChild>
                  <div className="flex items-center justify-between mb-4">
                    <div className="flex items-center gap-2">
                      <span className={category.color}>{category.icon}</span>
                      <h3 className="font-medium">{category.title}</h3>
                    </div>
                    <Info className="w-4 h-4 text-muted-foreground cursor-help" />
                  </div>
                </TooltipTrigger>
                <TooltipContent>
                  <p className="max-w-[250px]">{category.tooltip}</p>
                </TooltipContent>
              </Tooltip>
            </TooltipProvider>
            
            <div className="space-y-4">
              <div>
                <div className="flex items-center justify-between mb-2">
                  <p className="text-2xl font-bold">{formatCurrency(category.value)}</p>
                  <p className="text-lg font-semibold text-muted-foreground">
                    {formatPercentage(category.percentage / 100)}
                  </p>
                </div>
                <Progress 
                  value={category.percentage} 
                  className="h-2"
                  indicatorClassName={`bg-gradient-to-r ${
                    index === 0 
                      ? "from-blue-500 to-indigo-500"
                      : "from-violet-500 to-purple-500"
                  }`}
                />
              </div>

              <div className="space-y-3">
                {category.breakdown.map((item, itemIndex) => (
                  <MotionDiv
                    key={item.label}
                    initial={{ opacity: 0, x: -10 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ duration: 0.3, delay: 0.5 + itemIndex * 0.1 }}
                    className="bg-muted/30 rounded-lg p-3"
                  >
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-2">
                        <span className={item.color}>{item.icon}</span>
                        <p className="font-medium">{item.label}</p>
                      </div>
                      <p className="font-semibold">{formatCurrency(item.value)}</p>
                    </div>
                  </MotionDiv>
                ))}
              </div>
            </div>
          </MotionDiv>
        ))}
      </MotionDiv>

      {/* Investment Efficiency Metrics */}
      {investment_efficiency && (
        <MotionDiv
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.5, delay: 0.4 }}
          className="bg-gradient-to-br from-card to-muted/20 rounded-lg p-6 shadow-lg"
        >
          <div className="flex items-center gap-2 mb-4">
            <TrendingUp className="w-5 h-5 text-primary" />
            <h3 className="text-lg font-semibold">Investment Efficiency</h3>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <TooltipProvider>
              <Tooltip>
                <TooltipTrigger asChild>
                  <div className="bg-muted/30 rounded-lg p-4">
                    <div className="flex items-center gap-2">
                      <CircleDollarSign className="w-4 h-4 text-primary" />
                      <p className="text-sm text-muted-foreground">Investment per Unit</p>
                    </div>
                    <p className="text-xl font-bold mt-1">
                      {formatCurrency(investment_efficiency.per_unit)}
                    </p>
                  </div>
                </TooltipTrigger>
                <TooltipContent>
                  <p className="max-w-[250px]">Total investment divided by annual production capacity</p>
                </TooltipContent>
              </Tooltip>
            </TooltipProvider>

            <TooltipProvider>
              <Tooltip>
                <TooltipTrigger asChild>
                  <div className="bg-muted/30 rounded-lg p-4">
                    <div className="flex items-center gap-2">
                      <BarChart3 className="w-4 h-4 text-primary" />
                      <p className="text-sm text-muted-foreground">Revenue to Investment</p>
                    </div>
                    <div className="flex items-center gap-2 mt-1">
                      <p className="text-xl font-bold">{investment_efficiency.revenue_to_investment.toFixed(2)}x</p>
                      {investment_efficiency.revenue_to_investment > 1 ? (
                        <ArrowUpRight className="w-4 h-4 text-emerald-500" />
                      ) : (
                        <ArrowDownRight className="w-4 h-4 text-red-500" />
                      )}
                    </div>
                  </div>
                </TooltipTrigger>
                <TooltipContent>
                  <p className="max-w-[250px]">Annual revenue divided by total investment</p>
                </TooltipContent>
              </Tooltip>
            </TooltipProvider>

            <TooltipProvider>
              <Tooltip>
                <TooltipTrigger asChild>
                  <div className="bg-muted/30 rounded-lg p-4">
                    <div className="flex items-center gap-2">
                      <TrendingUp className="w-4 h-4 text-primary" />
                      <p className="text-sm text-muted-foreground">OPEX to CAPEX</p>
                    </div>
                    <div className="flex items-center gap-2 mt-1">
                      <p className="text-xl font-bold">{investment_efficiency.opex_to_capex.toFixed(2)}x</p>
                      {investment_efficiency.opex_to_capex < 1 ? (
                        <ArrowUpRight className="w-4 h-4 text-emerald-500" />
                      ) : (
                        <ArrowDownRight className="w-4 h-4 text-red-500" />
                      )}
                    </div>
                  </div>
                </TooltipTrigger>
                <TooltipContent>
                  <p className="max-w-[250px]">Ratio of annual operating expenses to capital expenditure</p>
                </TooltipContent>
              </Tooltip>
            </TooltipProvider>
          </div>
        </MotionDiv>
      )}
    </div>
  );
};
