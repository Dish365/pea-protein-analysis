import React from 'react';
import { Card, CardContent } from "@/components/ui/card";
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
  TrendingUp,
  CircleDollarSign,
  Timer,
  PieChart,
  BarChart3,
  Scale,
  Target,
  Activity,
  Package,
  Coins,
  Calculator,
  LineChart,
  AlertCircle,
  ArrowUpRight,
  ArrowDownRight,
  Info
} from 'lucide-react';

interface ProfitabilityMetricsProps {
  data: ComprehensiveAnalysisResponse;
}

export const ProfitabilityMetrics: React.FC<ProfitabilityMetricsProps> = ({ data }) => {
  const { profitability_analysis } = data;

  if (!profitability_analysis?.metrics) {
    return (
      <MotionDiv
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="bg-gradient-to-br from-background to-muted/20 rounded-lg p-6"
      >
        <div className="flex items-center gap-3 mb-4">
          <TrendingUp className="w-6 h-6 text-primary" />
          <h2 className="text-2xl font-bold">Profitability Analysis</h2>
        </div>
        <p className="text-muted-foreground">Profitability metrics not available</p>
      </MotionDiv>
    );
  }

  const { metrics } = profitability_analysis;
  const monteCarloResults = metrics.monte_carlo;

  const coreMetrics = [
    {
      title: "Net Present Value",
      value: formatCurrency(metrics.npv?.value),
      icon: <CircleDollarSign className="w-5 h-5" />,
      tooltip: "The current value of all future cash flows, discounted at the required rate of return",
      trend: metrics.npv?.value > 0 ? "positive" : "negative",
      color: "text-emerald-500"
    },
    {
      title: "Return on Investment",
      value: formatPercentage(metrics.roi?.value),
      icon: <TrendingUp className="w-5 h-5" />,
      tooltip: "The ratio of net profit to the cost of investment, expressed as a percentage",
      trend: metrics.roi?.value > 1 ? "positive" : "negative",
      color: "text-blue-500"
    },
    {
      title: "Payback Period",
      value: `${metrics.payback?.value.toFixed(2)} years`,
      icon: <Timer className="w-5 h-5" />,
      tooltip: "The time required to recover the cost of investment",
      trend: metrics.payback?.value < 5 ? "positive" : "negative",
      color: "text-purple-500"
    }
  ];

  const marginMetrics = [
    {
      title: "Gross Margin",
      value: formatPercentage(metrics.margins?.gross_margin?.value),
      icon: <Scale className="w-5 h-5" />,
      tooltip: "Revenue minus cost of goods sold, divided by revenue",
      color: "text-amber-500"
    },
    {
      title: "Operating Margin",
      value: formatPercentage(metrics.margins?.operating_margin?.value),
      icon: <Activity className="w-5 h-5" />,
      tooltip: "Operating income divided by revenue",
      color: "text-indigo-500"
    }
  ];

  return (
    <MotionDiv
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="space-y-6"
    >
      {/* Core Metrics */}
      <MotionDiv
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.5, delay: 0.2 }}
        className="grid grid-cols-1 md:grid-cols-3 gap-4"
      >
        {coreMetrics.map((metric, index) => (
          <MotionDiv
            key={metric.title}
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5, delay: index * 0.1 }}
            className="bg-gradient-to-br from-card to-muted/20 rounded-lg p-4 shadow-lg"
          >
            <TooltipProvider>
              <Tooltip>
                <TooltipTrigger asChild>
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <span className={metric.color}>{metric.icon}</span>
                      <h3 className="font-medium">{metric.title}</h3>
                    </div>
                    <Info className="w-4 h-4 text-muted-foreground cursor-help" />
                  </div>
                </TooltipTrigger>
                <TooltipContent>
                  <p className="max-w-[250px]">{metric.tooltip}</p>
                </TooltipContent>
              </Tooltip>
            </TooltipProvider>
            <div className="mt-2 flex items-center justify-between">
              <p className="text-2xl font-bold">{metric.value}</p>
              {metric.trend === "positive" ? (
                <ArrowUpRight className="w-5 h-5 text-emerald-500" />
              ) : (
                <ArrowDownRight className="w-5 h-5 text-red-500" />
              )}
            </div>
          </MotionDiv>
        ))}
      </MotionDiv>

      {/* Margins */}
      <MotionDiv
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.5, delay: 0.3 }}
        className="grid grid-cols-1 md:grid-cols-2 gap-4"
      >
        {marginMetrics.map((metric, index) => (
          <MotionDiv
            key={metric.title}
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5, delay: 0.4 + index * 0.1 }}
            className="bg-gradient-to-br from-card to-muted/20 rounded-lg p-4 shadow-lg"
          >
            <TooltipProvider>
              <Tooltip>
                <TooltipTrigger asChild>
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <span className={metric.color}>{metric.icon}</span>
                      <h3 className="font-medium">{metric.title}</h3>
                    </div>
                    <Info className="w-4 h-4 text-muted-foreground cursor-help" />
                  </div>
                </TooltipTrigger>
                <TooltipContent>
                  <p className="max-w-[250px]">{metric.tooltip}</p>
                </TooltipContent>
              </Tooltip>
            </TooltipProvider>
            <p className="mt-2 text-2xl font-bold">{metric.value}</p>
          </MotionDiv>
        ))}
      </MotionDiv>

      {/* Break-even Analysis */}
      {metrics.break_even && (
        <MotionDiv
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.5, delay: 0.4 }}
          className="bg-gradient-to-br from-card to-muted/20 rounded-lg p-6 shadow-lg"
        >
          <div className="flex items-center gap-2 mb-4">
            <Target className="w-5 h-5 text-primary" />
            <h3 className="text-lg font-semibold">Break-even Analysis</h3>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <TooltipProvider>
              <Tooltip>
                <TooltipTrigger asChild>
                  <div className="bg-muted/30 rounded-lg p-4">
                    <div className="flex items-center gap-2">
                      <Package className="w-4 h-4 text-primary" />
                      <p className="text-sm text-muted-foreground">Break-even Units</p>
                    </div>
                    <p className="text-xl font-bold mt-1">
                      {metrics.break_even.units.toLocaleString()}
                    </p>
                  </div>
                </TooltipTrigger>
                <TooltipContent>
                  <p className="max-w-[250px]">Number of units that need to be sold to cover all costs</p>
                </TooltipContent>
              </Tooltip>
            </TooltipProvider>

            <TooltipProvider>
              <Tooltip>
                <TooltipTrigger asChild>
                  <div className="bg-muted/30 rounded-lg p-4">
                    <div className="flex items-center gap-2">
                      <Coins className="w-4 h-4 text-primary" />
                      <p className="text-sm text-muted-foreground">Break-even Revenue</p>
                    </div>
                    <p className="text-xl font-bold mt-1">
                      {formatCurrency(metrics.break_even.revenue)}
                    </p>
                  </div>
                </TooltipTrigger>
                <TooltipContent>
                  <p className="max-w-[250px]">Revenue required to cover all costs</p>
                </TooltipContent>
              </Tooltip>
            </TooltipProvider>
          </div>
        </MotionDiv>
      )}

      {/* Monte Carlo Analysis */}
      {monteCarloResults && (
        <MotionDiv
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.5, delay: 0.5 }}
          className="bg-gradient-to-br from-card to-muted/20 rounded-lg p-6 shadow-lg"
        >
          <div className="flex items-center gap-2 mb-4">
            <Calculator className="w-5 h-5 text-primary" />
            <h3 className="text-lg font-semibold">Risk Analysis</h3>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <TooltipProvider>
              <Tooltip>
                <TooltipTrigger asChild>
                  <div className="bg-muted/30 rounded-lg p-4">
                    <div className="flex items-center gap-2">
                      <TrendingUp className="w-4 h-4 text-primary" />
                      <p className="text-sm text-muted-foreground">Mean NPV</p>
                    </div>
                    <p className="text-xl font-bold mt-1">
                      {formatCurrency(monteCarloResults.results.mean)}
                    </p>
                  </div>
                </TooltipTrigger>
                <TooltipContent>
                  <p className="max-w-[250px]">Average Net Present Value from Monte Carlo simulation</p>
                </TooltipContent>
              </Tooltip>
            </TooltipProvider>

            <TooltipProvider>
              <Tooltip>
                <TooltipTrigger asChild>
                  <div className="bg-muted/30 rounded-lg p-4">
                    <div className="flex items-center gap-2">
                      <Activity className="w-4 h-4 text-primary" />
                      <p className="text-sm text-muted-foreground">Risk (Std Dev)</p>
                    </div>
                    <p className="text-xl font-bold mt-1">
                      {formatCurrency(monteCarloResults.results.std_dev)}
                    </p>
                  </div>
                </TooltipTrigger>
                <TooltipContent>
                  <p className="max-w-[250px]">Standard deviation of NPV, indicating project risk</p>
                </TooltipContent>
              </Tooltip>
            </TooltipProvider>

            <div className="col-span-1 md:col-span-2">
              <TooltipProvider>
                <Tooltip>
                  <TooltipTrigger asChild>
                    <div className="bg-muted/30 rounded-lg p-4">
                      <div className="flex items-center gap-2">
                        <Scale className="w-4 h-4 text-primary" />
                        <p className="text-sm text-muted-foreground">95% Confidence Interval</p>
                      </div>
                      <p className="text-xl font-bold mt-1">
                        {formatCurrency(Array.isArray(monteCarloResults.results.confidence_interval)
                          ? monteCarloResults.results.confidence_interval[0]
                          : monteCarloResults.results.confidence_interval.lower)} to {formatCurrency(Array.isArray(monteCarloResults.results.confidence_interval)
                          ? monteCarloResults.results.confidence_interval[1]
                          : monteCarloResults.results.confidence_interval.upper)}
                      </p>
                    </div>
                  </TooltipTrigger>
                  <TooltipContent>
                    <p className="max-w-[250px]">Range within which NPV is expected to fall with 95% confidence</p>
                  </TooltipContent>
                </Tooltip>
              </TooltipProvider>
            </div>
          </div>
        </MotionDiv>
      )}
    </MotionDiv>
  );
};
