import React from 'react';
import { Card, CardContent } from "@/components/ui/card";
import { Separator } from "@/components/ui/separator";
import { ComprehensiveAnalysisResponse } from '@/types/economic';
import { formatCurrency, formatPercentage } from '@/utils/formatters';
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
  TrendingUp
} from 'lucide-react';

interface CostBreakdownProps {
  data: ComprehensiveAnalysisResponse;
}

export const CostBreakdown: React.FC<CostBreakdownProps> = ({ data }) => {
  const { capex_analysis, opex_analysis } = data;
  
  // Early return if essential data is missing
  if (!capex_analysis?.capex_summary || !opex_analysis?.opex_summary || !data.profitability_analysis?.metrics?.cost_structure) {
    return (
      <Card>
        <CardContent>
          <h2 className="text-2xl font-bold mb-4">
            Capital and Operational Expenditure
          </h2>
          <p className="text-muted-foreground">
            Cost breakdown data not available
          </p>
        </CardContent>
      </Card>
    );
  }

  const { capex_summary, working_capital_components, investment_efficiency } = capex_analysis;
  const { opex_summary } = opex_analysis;
  const { cost_structure } = data.profitability_analysis.metrics;

  return (
    <Card className="bg-gradient-to-br from-background to-muted/20">
      <CardContent className="p-6">
        <div className="flex items-center gap-2 mb-6">
          <CircleDollarSign className="w-6 h-6 text-primary" />
          <h2 className="text-2xl font-bold">
            Capital and Operational Expenditure
          </h2>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* CAPEX Section */}
          <div className="bg-card rounded-lg p-4 shadow-sm">
            <div className="flex items-center gap-2 mb-3">
              <Building2 className="w-5 h-5 text-primary" />
              <h3 className="text-lg font-semibold">
                Capital Expenditure
              </h3>
            </div>
            <div className="text-lg font-medium">
              Base CAPEX: {formatCurrency(capex_summary.total_capex)}
            </div>
          </div>

          {/* Working Capital Section */}
          {working_capital_components && (
            <div className="bg-card rounded-lg p-4 shadow-sm">
              <div className="flex items-center gap-2 mb-3">
                <Wallet className="w-5 h-5 text-primary" />
                <h3 className="text-lg font-semibold">
                  Working Capital Components
                </h3>
              </div>
              <div className="space-y-2">
                <div className="flex items-center gap-2">
                  <Package className="w-4 h-4 text-muted-foreground" />
                  <p>
                    Inventory ({working_capital_components.inventory.months} months): 
                    <span className="font-medium ml-1">{formatCurrency(working_capital_components.inventory.value)}</span>
                  </p>
                </div>
                <div className="flex items-center gap-2">
                  <Clock className="w-4 h-4 text-muted-foreground" />
                  <p>
                    Accounts Receivable ({working_capital_components.receivables.days} days): 
                    <span className="font-medium ml-1">{formatCurrency(working_capital_components.receivables.value)}</span>
                  </p>
                </div>
                <div className="flex items-center gap-2">
                  <Clock className="w-4 h-4 text-muted-foreground" />
                  <p>
                    Accounts Payable ({working_capital_components.payables.days} days): 
                    <span className="font-medium ml-1">{formatCurrency(working_capital_components.payables.value)}</span>
                  </p>
                </div>
                <div className="flex items-center gap-2 pt-2">
                  <BarChart3 className="w-4 h-4 text-primary" />
                  <p className="font-bold">
                    Net Working Capital: {formatCurrency(capex_summary.working_capital)}
                  </p>
                </div>
              </div>
            </div>
          )}

          {/* Investment Summary */}
          <div className="col-span-1 md:col-span-2 bg-primary/5 rounded-lg p-4">
            <div className="flex flex-col md:flex-row md:justify-between gap-4">
              <div className="flex items-center gap-2">
                <TrendingUp className="w-5 h-5 text-primary" />
                <p className="font-bold text-lg">
                  Total Investment: {formatCurrency(capex_summary.total_investment)}
                </p>
              </div>
              <div className="flex items-center gap-2">
                <CircleDollarSign className="w-5 h-5 text-primary" />
                <p className="text-lg">
                  Annual OPEX: {formatCurrency(opex_summary.total_opex)}
                </p>
              </div>
            </div>
          </div>

          {/* Cost Structure */}
          <div className="col-span-1 md:col-span-2 bg-card rounded-lg p-4 shadow-sm">
            <div className="flex items-center gap-2 mb-4">
              <BarChart3 className="w-5 h-5 text-primary" />
              <h3 className="text-lg font-semibold">
                Cost Structure
              </h3>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="bg-muted/30 rounded-lg p-4">
                <p className="font-semibold mb-3 flex items-center gap-2">
                  <span className="inline-block w-3 h-3 bg-primary rounded-full"></span>
                  Fixed Costs: {formatCurrency(data.profitability_analysis.metrics.cost_structure.fixed_costs.value)} 
                  <span className="text-muted-foreground">
                    ({formatPercentage(data.profitability_analysis.metrics.cost_structure.fixed_costs.percentage / 100)})
                  </span>
                </p>
                <div className="ml-4 space-y-2">
                  <div className="flex items-center gap-2">
                    <Users className="w-4 h-4 text-muted-foreground" />
                    <p>
                      Labor: {formatCurrency(data.profitability_analysis.metrics.cost_structure.fixed_costs.breakdown.labor)}
                    </p>
                  </div>
                  <div className="flex items-center gap-2">
                    <Wrench className="w-4 h-4 text-muted-foreground" />
                    <p>
                      Maintenance: {formatCurrency(data.profitability_analysis.metrics.cost_structure.fixed_costs.breakdown.maintenance)}
                    </p>
                  </div>
                </div>
              </div>
              <div className="bg-muted/30 rounded-lg p-4">
                <p className="font-semibold mb-3 flex items-center gap-2">
                  <span className="inline-block w-3 h-3 bg-secondary rounded-full"></span>
                  Variable Costs: {formatCurrency(data.profitability_analysis.metrics.cost_structure.variable_costs.value)} 
                  <span className="text-muted-foreground">
                    ({formatPercentage(data.profitability_analysis.metrics.cost_structure.variable_costs.percentage / 100)})
                  </span>
                </p>
                <div className="ml-4 space-y-2">
                  <div className="flex items-center gap-2">
                    <Package className="w-4 h-4 text-muted-foreground" />
                    <p>
                      Raw Materials: {formatCurrency(data.profitability_analysis.metrics.cost_structure.variable_costs.breakdown.raw_materials)}
                    </p>
                  </div>
                  <div className="flex items-center gap-2">
                    <Zap className="w-4 h-4 text-muted-foreground" />
                    <p>
                      Utilities: {formatCurrency(data.profitability_analysis.metrics.cost_structure.variable_costs.breakdown.utilities)}
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Investment Efficiency */}
          {investment_efficiency && (
            <div className="col-span-1 md:col-span-2 bg-card rounded-lg p-4 shadow-sm">
              <div className="flex items-center gap-2 mb-4">
                <TrendingUp className="w-5 h-5 text-primary" />
                <h3 className="text-lg font-semibold">
                  Investment Efficiency
                </h3>
              </div>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="bg-muted/30 rounded-lg p-3 flex items-center gap-2">
                  <CircleDollarSign className="w-4 h-4 text-primary" />
                  <p>
                    Investment per Unit: {formatCurrency(investment_efficiency.per_unit)}
                  </p>
                </div>
                <div className="bg-muted/30 rounded-lg p-3 flex items-center gap-2">
                  <BarChart3 className="w-4 h-4 text-primary" />
                  <p>
                    Revenue to Investment Ratio: {investment_efficiency.revenue_to_investment.toFixed(2)}
                  </p>
                </div>
                <div className="bg-muted/30 rounded-lg p-3 flex items-center gap-2">
                  <TrendingUp className="w-4 h-4 text-primary" />
                  <p>
                    OPEX to CAPEX Ratio: {investment_efficiency.opex_to_capex.toFixed(2)}
                  </p>
                </div>
              </div>
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  );
};
