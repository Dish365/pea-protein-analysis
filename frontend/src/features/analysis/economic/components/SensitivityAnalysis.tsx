"use client";

import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { formatCurrency } from '@/lib/formatters';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';

interface SensitivityAnalysisProps {
  npv: number;
  capex: {
    total_capex: number;
    equipment_cost: number;
  };
  opex: {
    total_opex: number;
  };
}

export function SensitivityAnalysis({
  npv,
  capex,
  opex,
}: SensitivityAnalysisProps) {
  // Generate sensitivity data points
  const generateSensitivityData = () => {
    const variations = [-20, -10, 0, 10, 20]; // Percentage variations
    return variations.map((variation) => {
      const factor = 1 + variation / 100;
      return {
        variation: `${variation > 0 ? '+' : ''}${variation}%`,
        capex: npv - (capex.total_capex * factor - capex.total_capex),
        opex: npv - (opex.total_opex * factor - opex.total_opex),
        baseline: npv,
      };
    });
  };

  const data = generateSensitivityData();

  return (
    <Card>
      <CardHeader>
        <CardTitle>Sensitivity Analysis</CardTitle>
        <p className="text-sm text-muted-foreground">
          Impact of cost variations on NPV
        </p>
      </CardHeader>
      <CardContent>
        <div className="h-[400px]">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={data} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="variation" />
              <YAxis
                tickFormatter={(value) => formatCurrency(value)}
                label={{
                  value: 'Net Present Value (NPV)',
                  angle: -90,
                  position: 'insideLeft',
                }}
              />
              <Tooltip
                formatter={(value: number) => formatCurrency(value)}
                labelFormatter={(label) => `Variation: ${label}`}
              />
              <Legend />
              <Line
                type="monotone"
                dataKey="capex"
                name="CAPEX Impact"
                stroke="#3b82f6"
                strokeWidth={2}
                dot={{ r: 4 }}
              />
              <Line
                type="monotone"
                dataKey="opex"
                name="OPEX Impact"
                stroke="#10b981"
                strokeWidth={2}
                dot={{ r: 4 }}
              />
              <Line
                type="monotone"
                dataKey="baseline"
                name="Baseline NPV"
                stroke="#6b7280"
                strokeDasharray="4 4"
                strokeWidth={2}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
        <div className="mt-4 grid grid-cols-3 gap-4">
          <div className="text-center">
            <p className="text-sm font-medium text-muted-foreground">Base NPV</p>
            <p className="text-lg font-semibold">{formatCurrency(npv)}</p>
          </div>
          <div className="text-center">
            <p className="text-sm font-medium text-muted-foreground">CAPEX Sensitivity</p>
            <p className="text-lg font-semibold text-blue-600">
              {formatCurrency(Math.abs(data[4].capex - data[0].capex))}
            </p>
          </div>
          <div className="text-center">
            <p className="text-sm font-medium text-muted-foreground">OPEX Sensitivity</p>
            <p className="text-lg font-semibold text-emerald-600">
              {formatCurrency(Math.abs(data[4].opex - data[0].opex))}
            </p>
          </div>
        </div>
      </CardContent>
    </Card>
  );
} 