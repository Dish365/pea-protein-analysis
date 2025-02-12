"use client";

import React from 'react';
import { Building2, Zap, DollarSign } from 'lucide-react';
import { formatCurrency } from '@/lib/formatters';
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from "@/components/ui/tooltip";
import { Progress } from "@/components/ui/progress";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";

interface CostBreakdownProps {
  capex: {
    total_capex: number;
    equipment_cost: number;
    installation_cost: number;
    indirect_cost: number;
  };
  opex: {
    total_opex: number;
    utilities_cost: number;
    materials_cost: number;
    labor_cost: number;
    maintenance_cost: number;
  };
  totalInvestment: number;
  annualCosts: number;
}

export function CostBreakdown({
  capex,
  opex,
  totalInvestment,
  annualCosts,
}: CostBreakdownProps) {
  const capexItems = [
    {
      title: 'Equipment',
      value: capex.equipment_cost,
      color: 'rgb(59 130 246)', // blue-500
      tooltip: 'Base equipment cost',
    },
    {
      title: 'Installation',
      value: capex.installation_cost,
      color: 'rgb(34 197 94)', // green-500
      tooltip: 'Equipment installation cost',
    },
    {
      title: 'Indirect Costs',
      value: capex.indirect_cost,
      color: 'rgb(234 179 8)', // yellow-500
      tooltip: 'Engineering, construction, and contingency costs',
    },
  ];

  const opexItems = [
    {
      title: 'Utilities',
      value: opex.utilities_cost,
      color: 'rgb(147 51 234)', // purple-500
      tooltip: 'Annual utility costs (electricity, water, etc.)',
    },
    {
      title: 'Materials',
      value: opex.materials_cost,
      color: 'rgb(236 72 153)', // pink-500
      tooltip: 'Annual raw material costs',
    },
    {
      title: 'Labor',
      value: opex.labor_cost,
      color: 'rgb(239 68 68)', // red-500
      tooltip: 'Annual labor costs',
    },
    {
      title: 'Maintenance',
      value: opex.maintenance_cost,
      color: 'rgb(249 115 22)', // orange-500
      tooltip: 'Annual maintenance costs',
    },
  ];

  const renderCostBreakdown = (items: typeof capexItems | typeof opexItems, total: number) => (
    <div className="space-y-4">
      {items.map((item, index) => (
        <TooltipProvider key={index}>
          <Tooltip>
            <TooltipTrigger asChild>
              <div className="space-y-2">
                <div className="flex justify-between text-sm">
                  <span className="font-medium">{item.title}</span>
                  <span className="text-muted-foreground">
                    {formatCurrency(item.value)} ({((item.value / total) * 100).toFixed(1)}%)
                  </span>
                </div>
                <Progress
                  value={(item.value / total) * 100}
                  indicatorColor={item.color}
                  className="h-2"
                />
              </div>
            </TooltipTrigger>
            <TooltipContent>
              <p>{item.tooltip}</p>
            </TooltipContent>
          </Tooltip>
        </TooltipProvider>
      ))}
    </div>
  );

  return (
    <Card>
      <CardHeader>
        <CardTitle>Cost Analysis</CardTitle>
      </CardHeader>
      <CardContent>
        <Tabs defaultValue="capex" className="space-y-4">
          <TabsList className="grid w-full grid-cols-2">
            <TabsTrigger value="capex" className="space-x-2">
              <Building2 className="h-4 w-4" />
              <span>Capital Expenditure</span>
            </TabsTrigger>
            <TabsTrigger value="opex" className="space-x-2">
              <Zap className="h-4 w-4" />
              <span>Operating Expenses</span>
            </TabsTrigger>
          </TabsList>

          <TabsContent value="capex" className="space-y-4">
            <Card>
              <CardContent className="pt-6">
                <div className="flex items-center gap-2">
                  <div className="rounded-full p-2 bg-primary/20">
                    <DollarSign className="h-4 w-4" />
                  </div>
                  <div>
                    <p className="text-sm font-medium text-muted-foreground">Total Investment</p>
                    <p className="text-2xl font-bold text-primary">{formatCurrency(totalInvestment)}</p>
                  </div>
                </div>
              </CardContent>
            </Card>
            {renderCostBreakdown(capexItems, totalInvestment)}
          </TabsContent>

          <TabsContent value="opex" className="space-y-4">
            <Card>
              <CardContent className="pt-6">
                <div className="flex items-center gap-2">
                  <div className="rounded-full p-2 bg-primary/20">
                    <DollarSign className="h-4 w-4" />
                  </div>
                  <div>
                    <p className="text-sm font-medium text-muted-foreground">Annual Operating Costs</p>
                    <p className="text-2xl font-bold text-primary">{formatCurrency(annualCosts)}</p>
                  </div>
                </div>
              </CardContent>
            </Card>
            {renderCostBreakdown(opexItems, annualCosts)}
          </TabsContent>
        </Tabs>
      </CardContent>
    </Card>
  );
} 