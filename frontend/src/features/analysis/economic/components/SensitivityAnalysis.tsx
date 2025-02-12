"use client";

import React from 'react';
import { Info } from 'lucide-react';
import { formatCurrency } from '@/lib/formatters';
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
import { Badge } from "@/components/ui/badge";

interface SensitivityParameter {
  parameter: string;
  baseValue: number;
  impact: number;
  sensitivity: 'Low' | 'Medium' | 'High';
  npvRange: [number, number];
  roiRange: [number, number];
}

interface SensitivityAnalysisProps {
  capex: {
    total_capex: number;
    equipment_cost: number;
  };
  opex: {
    total_opex: number;
  };
  profitability: {
    npv: number;
    roi: number;
    sensitivity_analysis?: {
      variables: string[];
      ranges: {
        [key: string]: {
          npv_impact: [number, number];
          roi_impact: [number, number];
          sensitivity: 'Low' | 'Medium' | 'High';
        };
      };
    };
  };
}

export function SensitivityAnalysis({
  capex,
  opex,
  profitability
}: SensitivityAnalysisProps) {
  // Transform backend data into table format
  const sensitivityData: SensitivityParameter[] = React.useMemo(() => {
    if (!profitability.sensitivity_analysis) return [];

    return Object.entries(profitability.sensitivity_analysis.ranges).map(([param, analysis]) => {
      // Calculate impact percentage on NPV
      const avgNpvImpact = ((analysis.npv_impact[1] - analysis.npv_impact[0]) / profitability.npv) * 100;

      return {
        parameter: param.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase()),
        baseValue: param === 'discount_rate' ? profitability.roi : 
                  param === 'production_volume' ? capex.total_capex : 
                  opex.total_opex,
        impact: Math.abs(avgNpvImpact),
        sensitivity: analysis.sensitivity,
        npvRange: analysis.npv_impact,
        roiRange: analysis.roi_impact
      };
    });
  }, [profitability, capex, opex]);

  const getSensitivityColor = (sensitivity: string) => {
    switch (sensitivity) {
      case 'High':
        return 'destructive';
      case 'Medium':
        return 'warning';
      default:
        return 'success';
    }
  };

  const getImpactColor = (impact: number) => {
    if (impact > 20) return 'text-destructive';
    if (impact > 10) return 'text-yellow-600';
    return 'text-emerald-600';
  };

  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
        <CardTitle>Sensitivity Analysis</CardTitle>
        <TooltipProvider>
          <Tooltip>
            <TooltipTrigger asChild>
              <Info className="h-4 w-4 text-muted-foreground" />
            </TooltipTrigger>
            <TooltipContent>
              <p>Analysis of how changes in key parameters affect project profitability</p>
            </TooltipContent>
          </Tooltip>
        </TooltipProvider>
      </CardHeader>
      <CardContent>
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Parameter</TableHead>
              <TableHead>Base Value</TableHead>
              <TableHead>NPV Range</TableHead>
              <TableHead>Impact on NPV</TableHead>
              <TableHead>Sensitivity</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {sensitivityData.map((record) => (
              <TableRow key={record.parameter}>
                <TableCell>
                  <div className="flex items-center gap-2">
                    {record.parameter}
                    <TooltipProvider>
                      <Tooltip>
                        <TooltipTrigger asChild>
                          <Info className="h-4 w-4 text-muted-foreground" />
                        </TooltipTrigger>
                        <TooltipContent>
                          <p>Impact of changes in {record.parameter.toLowerCase()} on profitability metrics</p>
                        </TooltipContent>
                      </Tooltip>
                    </TooltipProvider>
                  </div>
                </TableCell>
                <TableCell>
                  {record.parameter.includes('Rate') ? 
                    `${(record.baseValue * 100).toFixed(1)}%` : 
                    formatCurrency(record.baseValue)
                  }
                </TableCell>
                <TableCell>
                  <TooltipProvider>
                    <Tooltip>
                      <TooltipTrigger asChild>
                        <span>
                          {formatCurrency(record.npvRange[0])} to {formatCurrency(record.npvRange[1])}
                        </span>
                      </TooltipTrigger>
                      <TooltipContent>
                        <p>Potential NPV range based on parameter variation</p>
                      </TooltipContent>
                    </Tooltip>
                  </TooltipProvider>
                </TableCell>
                <TableCell>
                  <span className={getImpactColor(record.impact)}>
                    {record.impact >= 0 ? '+' : ''}{record.impact.toFixed(1)}%
                  </span>
                </TableCell>
                <TableCell>
                  <Badge variant={getSensitivityColor(record.sensitivity)}>
                    {record.sensitivity}
                  </Badge>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
          <tfoot>
            <TableRow>
              <TableCell colSpan={5} className="text-sm text-muted-foreground">
                * Sensitivity ranges are calculated using ±{(profitability.sensitivity_analysis?.ranges?.discount_rate?.sensitivity === 'High' ? 20 : 10)}% variation in parameters
              </TableCell>
            </TableRow>
          </tfoot>
        </Table>
      </CardContent>
    </Card>
  );
} 