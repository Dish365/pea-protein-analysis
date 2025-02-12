"use client";

import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { ParticleSizeDistribution } from '@/types/technical';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from 'recharts';

export interface ParticleSizeDisplayProps {
  distribution: ParticleSizeDistribution;
}

export function ParticleSizeDisplay({ distribution }: ParticleSizeDisplayProps) {
  const data = [
    {
      name: 'D10',
      value: distribution.d10,
      label: '10th Percentile',
    },
    {
      name: 'D50',
      value: distribution.d50,
      label: 'Median Size',
    },
    {
      name: 'D90',
      value: distribution.d90,
      label: '90th Percentile',
    },
  ];

  return (
    <Card>
      <CardHeader>
        <CardTitle>Particle Size Distribution</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="h-[300px]">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={data} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis label={{ value: 'Size (μm)', angle: -90, position: 'insideLeft' }} />
              <Tooltip
                content={({ active, payload }) => {
                  if (active && payload && payload.length) {
                    const data = payload[0].payload;
                    return (
                      <div className="rounded-lg bg-white p-2 shadow-md border">
                        <p className="font-medium">{data.label}</p>
                        <p className="text-sm text-muted-foreground">
                          {data.value.toFixed(1)} μm
                        </p>
                      </div>
                    );
                  }
                  return null;
                }}
              />
              <Bar
                dataKey="value"
                fill="#3b82f6"
                radius={[4, 4, 0, 0]}
              />
            </BarChart>
          </ResponsiveContainer>
        </div>
        <div className="mt-4 grid grid-cols-3 gap-4">
          {data.map((item) => (
            <div key={item.name} className="text-center">
              <p className="text-sm font-medium text-muted-foreground">{item.label}</p>
              <p className="text-lg font-semibold">{item.value.toFixed(1)} μm</p>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
} 