import React, { useState } from 'react';
import { Card, CardContent } from "@/components/ui/card";
import { ComprehensiveAnalysisResponse, SensitivityVariable } from '@/types/economic';
import { formatCurrency, formatPercentage } from '@/utils/formatters';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, ReferenceLine } from 'recharts';
import { Collapsible, CollapsibleContent, CollapsibleTrigger } from "@/components/ui/collapsible";
import { Button } from "@/components/ui/button";
import { 
  ChevronDown, 
  ChevronUp, 
  Table, 
  LineChart as LineChartIcon,
  ArrowUpRight,
  ArrowDownRight,
  ArrowRight,
  Info,
  TrendingUp,
  TrendingDown,
  MinusCircle
} from "lucide-react";
import { Badge } from "@/components/ui/badge";

interface SensitivityAnalysisProps {
  data: ComprehensiveAnalysisResponse;
}

export const SensitivityAnalysis: React.FC<SensitivityAnalysisProps> = ({ data }) => {
  const [openTables, setOpenTables] = useState<Record<string, boolean>>({});

  // Check if sensitivity analysis data exists and has results
  if (!data?.sensitivity_analysis?.sensitivity_analysis) {
    return (
      <Card className="bg-gradient-to-br from-background to-muted/20">
        <CardContent className="p-6">
          <div className="flex items-center gap-2 mb-6">
            <LineChartIcon className="w-6 h-6 text-primary" />
            <h2 className="text-2xl font-bold">
              Sensitivity Analysis
            </h2>
          </div>
          <p className="text-muted-foreground">
            No sensitivity analysis data available
          </p>
        </CardContent>
      </Card>
    );
  }

  const { sensitivity_analysis } = data.sensitivity_analysis;

  const toggleTable = (variable: string) => {
    setOpenTables(prev => ({
      ...prev,
      [variable]: !prev[variable]
    }));
  };

  const getImpactColor = (impact: number, variable: string) => {
    // For variables with inverse relationship (discount_rate, operating_costs)
    if (variable === 'discount_rate' || variable === 'operating_costs') {
      if (impact > 0) return 'text-green-600 font-semibold';  // Positive impact from decrease
      if (impact < -30) return 'text-red-600 font-semibold';  // High negative impact
      return 'text-yellow-600 font-semibold';  // Moderate negative impact
    }
    // For variables with direct relationship (production_volume, revenue)
    else {
      if (impact > 30) return 'text-green-600 font-semibold';  // High positive impact
      if (impact < 0) return 'text-red-600 font-semibold';     // Negative impact
      return 'text-yellow-600 font-semibold';  // Moderate positive impact
    }
  };

  const getImpactDescription = (impact: number, variable: string) => {
    const isInverse = variable === 'discount_rate' || variable === 'operating_costs';
    
    if (isInverse) {
      if (impact > 0) return `Positive Impact: Lower ${variable.split('_').join(' ')} increases NPV`;
      if (impact < -30) return `High Negative Impact: Higher ${variable.split('_').join(' ')} significantly decreases NPV`;
      return `Moderate Impact: Higher ${variable.split('_').join(' ')} moderately decreases NPV`;
    } else {
      if (impact > 30) return `High Positive Impact: Higher ${variable.split('_').join(' ')} significantly increases NPV`;
      if (impact < 0) return `Negative Impact: Lower ${variable.split('_').join(' ')} decreases NPV`;
      return `Moderate Impact: Higher ${variable.split('_').join(' ')} moderately increases NPV`;
    }
  };

  const getImpactIcon = (impact: number, variable: string) => {
    const isInverse = variable === 'discount_rate' || variable === 'operating_costs';
    
    if (isInverse) {
      if (impact > 0) return <TrendingUp className="w-4 h-4 text-green-600" />;
      if (impact < -30) return <TrendingDown className="w-4 h-4 text-red-600" />;
      return <MinusCircle className="w-4 h-4 text-yellow-600" />;
    } else {
      if (impact > 30) return <TrendingUp className="w-4 h-4 text-green-600" />;
      if (impact < 0) return <TrendingDown className="w-4 h-4 text-red-600" />;
      return <MinusCircle className="w-4 h-4 text-yellow-600" />;
    }
  };

  const formatYAxisTick = (value: number) => {
    if (value === 0) return '$0';
    if (Math.abs(value) >= 1000000) {
      return `$${(value / 1000000).toFixed(1)}M`;
    }
    if (Math.abs(value) >= 1000) {
      return `$${(value / 1000).toFixed(1)}K`;
    }
    return `$${value}`;
  };

  return (
    <Card className="bg-gradient-to-br from-background to-muted/20">
      <CardContent className="p-6">
        <div className="flex items-center gap-2 mb-6">
          <LineChartIcon className="w-6 h-6 text-primary" />
          <h2 className="text-2xl font-bold">
            Sensitivity Analysis
          </h2>
        </div>

        <div className="space-y-8">
          {Object.entries(sensitivity_analysis).map(([variable, data]: [string, SensitivityVariable]) => {
            if (!data?.values) return null;
            
            const baseIndex = data.percent_change.findIndex(
              (change: number, i: number, arr: number[]) => Math.abs(change) === Math.min(...arr.map(Math.abs))
            );

            const maxImpact = (variable === 'discount_rate' || variable === 'operating_costs')
              ? data.percent_change.reduce((max, current) => 
                  current < max ? current : max
                )
              : Math.max(...data.percent_change);

            const chartData = data.percent_change.map((change, index) => ({
              impact: change.toFixed(1),
              npv: data.values[index]
            }));
            
            return (
              <div 
                key={variable} 
                className="bg-card rounded-lg p-6 shadow-lg border border-border/50 hover:shadow-xl transition-shadow duration-200"
              >
                <div className="flex items-center justify-between mb-6">
                  <div className="space-y-3">
                    <h3 className="text-2xl font-semibold flex items-center gap-3">
                      {variable.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ')}
                      <div className="p-1.5 rounded-full bg-muted">
                        {getImpactIcon(maxImpact, variable)}
                      </div>
                    </h3>
                    <div className="flex flex-wrap gap-4 items-center">
                      <Badge 
                        variant={
                          (variable === 'discount_rate' || variable === 'operating_costs')
                            ? (maxImpact > 0 ? "success" : maxImpact < -30 ? "destructive" : "warning")
                            : (maxImpact > 30 ? "success" : maxImpact < 0 ? "destructive" : "warning")
                        }
                        className="flex items-center gap-2 px-3 py-1.5 text-sm"
                      >
                        <Info className="w-4 h-4" />
                        Max Impact: {maxImpact.toFixed(1)}%
                      </Badge>
                      <div className="px-3 py-1.5 bg-muted/30 rounded-full flex items-center gap-2">
                        <LineChartIcon className="w-4 h-4 text-primary" />
                        <span className="text-sm font-medium">
                          Base NPV: {formatCurrency(data.values[baseIndex])}
                        </span>
                      </div>
                    </div>
                  </div>
                </div>

                {/* Legend */}
                <div className="flex flex-wrap gap-4 text-sm mb-6 bg-muted/30 p-4 rounded-lg backdrop-blur-sm">
                  {(variable === 'discount_rate' || variable === 'operating_costs') ? (
                    <>
                      <span className="flex items-center gap-2 px-3 py-1.5 bg-background/50 rounded-full">
                        <ArrowDownRight className="w-4 h-4 text-green-600" />
                        <span className="text-muted-foreground">
                          Decrease: NPV Increases
                        </span>
                      </span>
                      <span className="flex items-center gap-2 px-3 py-1.5 bg-background/50 rounded-full">
                        <ArrowRight className="w-4 h-4 text-yellow-600" />
                        <span className="text-muted-foreground">
                          Small Increase: NPV Slightly Decreases
                        </span>
                      </span>
                      <span className="flex items-center gap-2 px-3 py-1.5 bg-background/50 rounded-full">
                        <ArrowUpRight className="w-4 h-4 text-red-600" />
                        <span className="text-muted-foreground">
                          Large Increase: NPV Significantly Decreases
                        </span>
                      </span>
                    </>
                  ) : (
                    <>
                      <span className="flex items-center gap-2 px-3 py-1.5 bg-background/50 rounded-full">
                        <ArrowUpRight className="w-4 h-4 text-green-600" />
                        <span className="text-muted-foreground">
                          Large Increase: NPV Significantly Increases
                        </span>
                      </span>
                      <span className="flex items-center gap-2 px-3 py-1.5 bg-background/50 rounded-full">
                        <ArrowRight className="w-4 h-4 text-yellow-600" />
                        <span className="text-muted-foreground">
                          Small Increase: NPV Slightly Increases
                        </span>
                      </span>
                      <span className="flex items-center gap-2 px-3 py-1.5 bg-background/50 rounded-full">
                        <ArrowDownRight className="w-4 h-4 text-red-600" />
                        <span className="text-muted-foreground">
                          Decrease: NPV Decreases
                        </span>
                      </span>
                    </>
                  )}
                </div>

                {/* Chart */}
                <div className="bg-card rounded-lg p-6 shadow-sm mb-6 border border-border/50">
                  <ResponsiveContainer width="100%" height={400}>
                    <LineChart data={chartData} margin={{ top: 20, right: 50, left: 80, bottom: 20 }}>
                      <CartesianGrid strokeDasharray="3 3" stroke="#E5E7EB" />
                      <XAxis 
                        dataKey="impact" 
                        label={{ value: 'Impact on NPV (%)', position: 'bottom', offset: 0 }}
                        tick={{ fill: '#6B7280' }}
                      />
                      <YAxis 
                        label={{ value: 'NPV ($)', angle: -90, position: 'insideLeft', offset: -10 }}
                        tickFormatter={formatYAxisTick}
                        tick={{ fill: '#6B7280' }}
                        width={75}
                      />
                      <Tooltip 
                        contentStyle={{ 
                          backgroundColor: 'white', 
                          borderRadius: '8px', 
                          border: '1px solid #E5E7EB',
                          boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
                        }}
                        formatter={(value: any, name: string) => {
                          if (name === 'NPV') return [formatCurrency(value), 'NPV'];
                          return [`${Number(value).toFixed(1)}%`, 'Impact'];
                        }}
                        labelFormatter={(label) => `Impact: ${label}%`}
                      />
                      <ReferenceLine y={data.values[baseIndex]} stroke="#9CA3AF" strokeDasharray="3 3" />
                      <ReferenceLine x="0.0" stroke="#9CA3AF" strokeDasharray="3 3" />
                      <Line 
                        type="monotone" 
                        dataKey="npv" 
                        name="NPV"
                        stroke="#2563eb" 
                        strokeWidth={2}
                        dot={{ fill: '#2563eb', r: 2 }}
                        activeDot={{ r: 6, stroke: '#2563eb', strokeWidth: 2 }}
                      />
                    </LineChart>
                  </ResponsiveContainer>
                </div>

                {/* Collapsible Table */}
                <Collapsible open={openTables[variable]} onOpenChange={() => toggleTable(variable)}>
                  <CollapsibleTrigger asChild>
                    <Button 
                      variant="outline" 
                      className="w-full flex items-center justify-center gap-2 hover:bg-muted/50 transition-colors"
                    >
                      <Table className="h-4 w-4" />
                      {openTables[variable] ? 'Hide' : 'Show'} Detailed Data
                      {openTables[variable] ? <ChevronUp className="h-4 w-4" /> : <ChevronDown className="h-4 w-4" />}
                    </Button>
                  </CollapsibleTrigger>
                  <CollapsibleContent>
                    <div className="mt-4 overflow-x-auto rounded-lg border bg-card">
                      <table className="w-full">
                        <thead>
                          <tr className="bg-muted/50 border-b">
                            <th className="text-left py-3 px-4 font-semibold">Impact on NPV (%)</th>
                            <th className="text-left py-3 px-4 font-semibold">NPV</th>
                          </tr>
                        </thead>
                        <tbody>
                          {data.percent_change.map((change: number, index: number) => (
                            <tr 
                              key={index} 
                              className={`
                                border-t
                                ${index === baseIndex ? "bg-muted/50" : "hover:bg-muted/30"}
                                transition-colors
                              `}
                            >
                              <td className={`py-3 px-4 ${index !== baseIndex ? getImpactColor(change, variable) : ''}`}>
                                {index === baseIndex ? (
                                  <Badge variant="outline" className="bg-primary/5">Base Case</Badge>
                                ) : (
                                  <div className="flex items-center gap-2">
                                    {getImpactIcon(change, variable)}
                                    {change.toFixed(1)}%
                                  </div>
                                )}
                              </td>
                              <td className="py-3 px-4 font-medium">{formatCurrency(data.values[index])}</td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                  </CollapsibleContent>
                </Collapsible>
              </div>
            );
          })}
        </div>
      </CardContent>
    </Card>
  );
};
