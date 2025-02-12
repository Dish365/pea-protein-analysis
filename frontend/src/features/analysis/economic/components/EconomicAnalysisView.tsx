"use client";

import React from 'react';
import { DollarSign, TrendingUp, Clock, Percent } from 'lucide-react';
import { formatCurrency } from '@/lib/formatters';
import { EconomicAnalysisResult } from '@/types/economic';
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from "@/components/ui/tooltip";
import { Progress } from "@/components/ui/progress";

interface EconomicAnalysisViewProps {
  data: EconomicAnalysisResult;
}

export function EconomicAnalysisView({ data }: EconomicAnalysisViewProps) {
  // Key financial metrics
  const keyMetrics = [
    {
      title: 'Net Present Value',
      value: data.profitability_analysis.npv,
      icon: <DollarSign className="h-4 w-4" />,
      suffix: 'USD',
      precision: 0,
      color: data.profitability_analysis.npv > 0 ? 'text-emerald-600' : 'text-destructive'
    },
    {
      title: 'Return on Investment',
      value: data.profitability_analysis.roi,
      icon: <Percent className="h-4 w-4" />,
      suffix: '%',
      precision: 1,
      color: data.profitability_analysis.roi > 15 ? 'text-emerald-600' : 'text-yellow-600'
    },
    {
      title: 'Payback Period',
      value: data.profitability_analysis.payback_period,
      icon: <Clock className="h-4 w-4" />,
      suffix: 'years',
      precision: 1,
      color: data.profitability_analysis.payback_period < 5 ? 'text-emerald-600' : 'text-yellow-600'
    },
    {
      title: 'IRR',
      value: data.profitability_analysis.irr,
      icon: <TrendingUp className="h-4 w-4" />,
      suffix: '%',
      precision: 1,
      color: data.profitability_analysis.irr > 20 ? 'text-emerald-600' : 'text-yellow-600'
    }
  ];

  // CAPEX breakdown data
  const capexData = [
    {
      key: 'equipment',
      category: 'Equipment Cost',
      amount: data.capex_analysis.equipment_cost,
      percentage: (data.capex_analysis.equipment_cost / data.capex_analysis.total_capex) * 100
    },
    {
      key: 'installation',
      category: 'Installation Cost',
      amount: data.capex_analysis.installation_cost,
      percentage: (data.capex_analysis.installation_cost / data.capex_analysis.total_capex) * 100
    },
    {
      key: 'indirect',
      category: 'Indirect Cost',
      amount: data.capex_analysis.indirect_cost,
      percentage: (data.capex_analysis.indirect_cost / data.capex_analysis.total_capex) * 100
    }
  ];

  // OPEX breakdown data
  const opexData = [
    {
      key: 'utilities',
      category: 'Utilities',
      amount: data.opex_analysis.utilities_cost,
      percentage: (data.opex_analysis.utilities_cost / data.opex_analysis.total_opex) * 100
    },
    {
      key: 'materials',
      category: 'Materials',
      amount: data.opex_analysis.materials_cost,
      percentage: (data.opex_analysis.materials_cost / data.opex_analysis.total_opex) * 100
    },
    {
      key: 'labor',
      category: 'Labor',
      amount: data.opex_analysis.labor_cost,
      percentage: (data.opex_analysis.labor_cost / data.opex_analysis.total_opex) * 100
    },
    {
      key: 'maintenance',
      category: 'Maintenance',
      amount: data.opex_analysis.maintenance_cost,
      percentage: (data.opex_analysis.maintenance_cost / data.opex_analysis.total_opex) * 100
    }
  ];

  const renderMetricCard = (metric: typeof keyMetrics[0]) => (
    <Card>
      <CardContent className="pt-6">
        <div className="flex items-center gap-2">
          <div className={`rounded-full p-2 ${metric.color.replace('text', 'bg')}/20`}>
            {metric.icon}
          </div>
          <div>
            <p className="text-sm font-medium text-muted-foreground">{metric.title}</p>
            <p className={`text-2xl font-bold ${metric.color}`}>
              {metric.suffix === 'USD' 
                ? formatCurrency(metric.value)
                : `${metric.value.toFixed(metric.precision)}${metric.suffix}`}
            </p>
          </div>
        </div>
      </CardContent>
    </Card>
  );

  const renderCostTable = (data: typeof capexData | typeof opexData) => (
    <Table>
      <TableHeader>
        <TableRow>
          <TableHead>Category</TableHead>
          <TableHead>Amount (USD)</TableHead>
          <TableHead>Percentage</TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        {data.map((item) => (
          <TableRow key={item.key}>
            <TableCell>{item.category}</TableCell>
            <TableCell>{formatCurrency(item.amount)}</TableCell>
            <TableCell>
              <TooltipProvider>
                <Tooltip>
                  <TooltipTrigger asChild>
                    <div className="w-full max-w-[200px]">
                      <Progress 
                        value={item.percentage} 
                        className="h-2"
                        indicatorColor={item.percentage > 50 ? 'rgb(59 130 246)' : 'rgb(99 102 241)'}
                      />
                    </div>
                  </TooltipTrigger>
                  <TooltipContent>
                    <p>{item.percentage.toFixed(1)}%</p>
                  </TooltipContent>
                </Tooltip>
              </TooltipProvider>
            </TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  );

  return (
    <div className="space-y-6">
      <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
        {keyMetrics.map((metric, index) => (
          <div key={index}>
            {renderMetricCard(metric)}
          </div>
        ))}
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle>Capital Expenditure (CAPEX) Breakdown</CardTitle>
            <p className="text-2xl font-bold text-primary">
              {formatCurrency(data.capex_analysis.total_capex)}
            </p>
          </CardHeader>
          <CardContent>
            {renderCostTable(capexData)}
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Operating Expenditure (OPEX) Breakdown</CardTitle>
            <p className="text-2xl font-bold text-primary">
              {formatCurrency(data.opex_analysis.total_opex)}
            </p>
          </CardHeader>
          <CardContent>
            {renderCostTable(opexData)}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}