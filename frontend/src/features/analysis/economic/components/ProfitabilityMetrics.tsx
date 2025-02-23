import React from 'react';
import { Card, CardContent } from "@/components/ui/card";
import { Separator } from "@/components/ui/separator";
import { ComprehensiveAnalysisResponse } from '@/types/economic';
import { formatCurrency, formatPercentage } from '@/utils/formatters';
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
  AlertCircle
} from 'lucide-react';

interface ProfitabilityMetricsProps {
  data: ComprehensiveAnalysisResponse;
}

export const ProfitabilityMetrics: React.FC<ProfitabilityMetricsProps> = ({ data }) => {
  const { profitability_analysis } = data;

  // Early return if essential data is missing
  if (!profitability_analysis?.metrics) {
    return (
      <Card className="bg-gradient-to-br from-background to-muted/20">
        <CardContent className="p-6">
          <div className="flex items-center gap-2 mb-6">
            <TrendingUp className="w-6 h-6 text-primary" />
            <h2 className="text-2xl font-bold">
              Profitability Analysis
            </h2>
          </div>
          <p className="text-muted-foreground">
            Profitability metrics not available
          </p>
        </CardContent>
      </Card>
    );
  }

  const { metrics } = profitability_analysis;
  const monteCarloResults = metrics.monte_carlo;

  return (
    <Card className="bg-gradient-to-br from-background to-muted/20">
      <CardContent className="p-6">
        <div className="flex items-center gap-2 mb-6">
          <TrendingUp className="w-6 h-6 text-primary" />
          <h2 className="text-2xl font-bold">
            Profitability Analysis
          </h2>
        </div>

        <div className="space-y-6">
          {/* Core Metrics */}
          <div className="bg-card rounded-lg p-4 shadow-sm">
            <div className="flex items-center gap-2 mb-4">
              <Target className="w-5 h-5 text-primary" />
              <h3 className="text-lg font-semibold">
                Core Profitability Metrics
              </h3>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="bg-muted/30 rounded-lg p-3 flex items-center gap-3">
                <CircleDollarSign className="w-5 h-5 text-primary" />
                <div>
                  <p className="text-sm text-muted-foreground">NPV</p>
                  <p className="font-medium">{formatCurrency(metrics.npv?.value)}</p>
                </div>
              </div>
              <div className="bg-muted/30 rounded-lg p-3 flex items-center gap-3">
                <TrendingUp className="w-5 h-5 text-primary" />
                <div>
                  <p className="text-sm text-muted-foreground">ROI</p>
                  <p className="font-medium">{formatPercentage(metrics.roi?.value)}</p>
                </div>
              </div>
              <div className="bg-muted/30 rounded-lg p-3 flex items-center gap-3">
                <Timer className="w-5 h-5 text-primary" />
                <div>
                  <p className="text-sm text-muted-foreground">Payback Period</p>
                  <p className="font-medium">{metrics.payback?.value.toFixed(2)} years</p>
                </div>
              </div>
            </div>
          </div>

          {/* Margins */}
          {metrics.margins && (
            <div className="bg-card rounded-lg p-4 shadow-sm">
              <div className="flex items-center gap-2 mb-4">
                <PieChart className="w-5 h-5 text-primary" />
                <h3 className="text-lg font-semibold">
                  Margins
                </h3>
              </div>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="bg-muted/30 rounded-lg p-3 flex items-center gap-3">
                  <Scale className="w-5 h-5 text-primary" />
                  <div>
                    <p className="text-sm text-muted-foreground">Gross Margin</p>
                    <p className="font-medium">{formatPercentage(metrics.margins.gross_margin?.value)}</p>
                  </div>
                </div>
                <div className="bg-muted/30 rounded-lg p-3 flex items-center gap-3">
                  <Activity className="w-5 h-5 text-primary" />
                  <div>
                    <p className="text-sm text-muted-foreground">Operating Margin</p>
                    <p className="font-medium">{formatPercentage(metrics.margins.operating_margin?.value)}</p>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Annual Performance */}
          {metrics.annual_metrics && (
            <div className="bg-card rounded-lg p-4 shadow-sm">
              <div className="flex items-center gap-2 mb-4">
                <BarChart3 className="w-5 h-5 text-primary" />
                <h3 className="text-lg font-semibold">
                  Annual Performance
                </h3>
              </div>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="bg-muted/30 rounded-lg p-3 flex items-center gap-3">
                  <Coins className="w-5 h-5 text-primary" />
                  <div>
                    <p className="text-sm text-muted-foreground">Revenue</p>
                    <p className="font-medium">{formatCurrency(metrics.annual_metrics.revenue)}</p>
                  </div>
                </div>
                <div className="bg-muted/30 rounded-lg p-3 flex items-center gap-3">
                  <CircleDollarSign className="w-5 h-5 text-primary" />
                  <div>
                    <p className="text-sm text-muted-foreground">Operating Costs</p>
                    <p className="font-medium">{formatCurrency(metrics.annual_metrics.operating_costs)}</p>
                  </div>
                </div>
                <div className="bg-muted/30 rounded-lg p-3 flex items-center gap-3">
                  <Calculator className="w-5 h-5 text-primary" />
                  <div>
                    <p className="text-sm text-muted-foreground">Total Costs</p>
                    <p className="font-medium">{formatCurrency(metrics.annual_metrics.total_costs)}</p>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Break-even Analysis */}
          {metrics.break_even && (
            <div className="bg-card rounded-lg p-4 shadow-sm">
              <div className="flex items-center gap-2 mb-4">
                <Target className="w-5 h-5 text-primary" />
                <h3 className="text-lg font-semibold">
                  Break-even Analysis
                </h3>
              </div>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="bg-muted/30 rounded-lg p-3 flex items-center gap-3">
                  <Package className="w-5 h-5 text-primary" />
                  <div>
                    <p className="text-sm text-muted-foreground">Break-even Units</p>
                    <p className="font-medium">{metrics.break_even.units.toLocaleString()}</p>
                  </div>
                </div>
                <div className="bg-muted/30 rounded-lg p-3 flex items-center gap-3">
                  <Coins className="w-5 h-5 text-primary" />
                  <div>
                    <p className="text-sm text-muted-foreground">Break-even Revenue</p>
                    <p className="font-medium">{formatCurrency(metrics.break_even.revenue)}</p>
                  </div>
                </div>
              </div>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4">
                <div className="bg-muted/30 rounded-lg p-3 flex items-center gap-3">
                  <CircleDollarSign className="w-5 h-5 text-primary" />
                  <div>
                    <p className="text-sm text-muted-foreground">Unit Price</p>
                    <p className="font-medium">{formatCurrency(metrics.break_even.unit_price)}</p>
                  </div>
                </div>
                <div className="bg-muted/30 rounded-lg p-3 flex items-center gap-3">
                  <Calculator className="w-5 h-5 text-primary" />
                  <div>
                    <p className="text-sm text-muted-foreground">Variable Cost per Unit</p>
                    <p className="font-medium">{formatCurrency(metrics.break_even.variable_cost_per_unit)}</p>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Additional Business Insights */}
          {metrics.annual_metrics && (
            <div className="bg-card rounded-lg p-4 shadow-sm">
              <div className="flex items-center gap-2 mb-4">
                <LineChart className="w-5 h-5 text-primary" />
                <h3 className="text-lg font-semibold">
                  Additional Business Insights
                </h3>
              </div>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="bg-muted/30 rounded-lg p-3 flex items-center gap-3">
                  <Package className="w-5 h-5 text-primary" />
                  <div>
                    <p className="text-sm text-muted-foreground">Effective Production</p>
                    <p className="font-medium">{metrics.annual_metrics.effective_production.toLocaleString()} units</p>
                  </div>
                </div>
                <div className="bg-muted/30 rounded-lg p-3 flex items-center gap-3">
                  <CircleDollarSign className="w-5 h-5 text-primary" />
                  <div>
                    <p className="text-sm text-muted-foreground">CAPEX per Unit</p>
                    <p className="font-medium">{formatCurrency(data.capex_analysis.investment_efficiency?.per_unit || 0)}</p>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Risk Analysis */}
          {monteCarloResults && (
            <div className="bg-card rounded-lg p-4 shadow-sm">
              <div className="flex items-center gap-2 mb-4">
                <AlertCircle className="w-5 h-5 text-primary" />
                <h3 className="text-lg font-semibold">
                  Risk Analysis
                </h3>
              </div>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="bg-muted/30 rounded-lg p-3 flex items-center gap-3">
                  <Activity className="w-5 h-5 text-primary" />
                  <div>
                    <p className="text-sm text-muted-foreground">NPV Risk (Std Dev)</p>
                    <p className="font-medium">{formatCurrency(monteCarloResults.results.std_dev)}</p>
                  </div>
                </div>
                <div className="bg-muted/30 rounded-lg p-3 flex items-center gap-3">
                  <Scale className="w-5 h-5 text-primary" />
                  <div>
                    <p className="text-sm text-muted-foreground">NPV Range</p>
                    <p className="font-medium">
                      {formatCurrency(Array.isArray(monteCarloResults.results.confidence_interval) 
                        ? monteCarloResults.results.confidence_interval[0] 
                        : monteCarloResults.results.confidence_interval.lower)} to {formatCurrency(Array.isArray(monteCarloResults.results.confidence_interval)
                        ? monteCarloResults.results.confidence_interval[1]
                        : monteCarloResults.results.confidence_interval.upper)}
                    </p>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Monte Carlo Analysis */}
          {monteCarloResults && (
            <div className="bg-card rounded-lg p-4 shadow-sm">
              <div className="flex items-center gap-2 mb-4">
                <Calculator className="w-5 h-5 text-primary" />
                <h3 className="text-lg font-semibold">
                  Monte Carlo Analysis
                </h3>
              </div>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="bg-muted/30 rounded-lg p-3 flex items-center gap-3">
                  <TrendingUp className="w-5 h-5 text-primary" />
                  <div>
                    <p className="text-sm text-muted-foreground">Mean NPV</p>
                    <p className="font-medium">{formatCurrency(monteCarloResults.results.mean)}</p>
                  </div>
                </div>
                <div className="bg-muted/30 rounded-lg p-3 flex items-center gap-3">
                  <Activity className="w-5 h-5 text-primary" />
                  <div>
                    <p className="text-sm text-muted-foreground">Standard Deviation</p>
                    <p className="font-medium">{formatCurrency(monteCarloResults.results.std_dev)}</p>
                  </div>
                </div>
                <div className="col-span-1 md:col-span-2 bg-muted/30 rounded-lg p-3">
                  <div className="flex items-center gap-3">
                    <Scale className="w-5 h-5 text-primary" />
                    <div>
                      <p className="text-sm text-muted-foreground">95% Confidence Interval</p>
                      <p className="font-medium">
                        {formatCurrency(Array.isArray(monteCarloResults.results.confidence_interval)
                          ? monteCarloResults.results.confidence_interval[0]
                          : monteCarloResults.results.confidence_interval.lower)} to {formatCurrency(Array.isArray(monteCarloResults.results.confidence_interval)
                          ? monteCarloResults.results.confidence_interval[1]
                          : monteCarloResults.results.confidence_interval.upper)}
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  );
};
