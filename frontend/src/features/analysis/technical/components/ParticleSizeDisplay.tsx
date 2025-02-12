"use client";

import React from 'react';
import { HelpCircle, Activity } from 'lucide-react';
import { DataTable } from "@/components/ui/data-table";
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
import { Badge } from "@/components/ui/badge";
import { type Row } from "@tanstack/react-table";

interface ParticleSizeDisplayProps {
  d10: number;
  d50: number;
  d90: number;
  span: number;
}

interface DataType {
  key: string;
  metric: string;
  value: number;
  tooltip: string;
  status?: {
    text: string;
    color: string;
  };
}

export function ParticleSizeDisplay({
  d10,
  d50,
  d90,
  span,
}: ParticleSizeDisplayProps) {
  const getDistributionQuality = (span: number) => {
    if (span <= 1.5) return { text: 'Excellent', color: 'success' };
    if (span <= 2.0) return { text: 'Good', color: 'processing' };
    if (span <= 2.5) return { text: 'Fair', color: 'warning' };
    return { text: 'Poor', color: 'error' };
  };

  const getParticleRange = (d10: number, d90: number) => {
    const range = d90 - d10;
    if (range <= 50) return { text: 'Narrow', color: 'success' };
    if (range <= 100) return { text: 'Moderate', color: 'processing' };
    if (range <= 150) return { text: 'Wide', color: 'warning' };
    return { text: 'Very Wide', color: 'error' };
  };

  const quality = getDistributionQuality(span);
  const range = getParticleRange(d10, d90);

  const data: DataType[] = [
    {
      key: 'd10',
      metric: 'D10 (Fine Particles)',
      value: d10,
      tooltip: '10% of particles are smaller than this size',
    },
    {
      key: 'd50',
      metric: 'D50 (Median Size)',
      value: d50,
      tooltip: 'Median particle size (50% are smaller/larger)',
    },
    {
      key: 'd90',
      metric: 'D90 (Coarse Particles)',
      value: d90,
      tooltip: '90% of particles are smaller than this size',
    },
    {
      key: 'span',
      metric: 'Distribution Span',
      value: span,
      tooltip: 'Measure of distribution width (D90-D10)/D50',
      status: quality,
    },
  ];

  const columns = [
    {
      accessorKey: 'metric',
      header: 'Metric',
      cell: ({ row }: { row: Row<DataType> }) => (
        <TooltipProvider>
          <Tooltip>
            <TooltipTrigger asChild>
              <div className="flex items-center gap-2">
                {row.original.metric}
                <HelpCircle className="h-4 w-4" />
              </div>
            </TooltipTrigger>
            <TooltipContent>
              <p>{row.original.tooltip}</p>
            </TooltipContent>
          </Tooltip>
        </TooltipProvider>
      ),
    },
    {
      accessorKey: 'value',
      header: 'Value',
      cell: ({ row }: { row: Row<DataType> }) => `${row.original.value.toFixed(1)} μm`,
    },
    {
      accessorKey: 'status',
      header: 'Status',
      cell: ({ row }: { row: Row<DataType> }) => {
        const status = row.original.status;
        if (!status) return null;
        return (
          <Badge
            variant={
              status.color === 'success' ? 'success' :
              status.color === 'processing' ? 'default' :
              status.color === 'warning' ? 'warning' : 'destructive'
            }
          >
            {status.text}
          </Badge>
        );
      },
    },
  ];

  return (
    <Card>
      <CardHeader>
        <div className="flex items-center justify-between">
          <CardTitle>Particle Size Distribution</CardTitle>
          <div className="flex gap-2">
            <TooltipProvider>
              <Tooltip>
                <TooltipTrigger asChild>
                  <Badge
                    variant={
                      quality.color === 'success' ? 'success' :
                      quality.color === 'processing' ? 'default' :
                      quality.color === 'warning' ? 'warning' : 'destructive'
                    }
                  >
                    {quality.text} Distribution
                  </Badge>
                </TooltipTrigger>
                <TooltipContent>
                  <p>Distribution quality</p>
                </TooltipContent>
              </Tooltip>
            </TooltipProvider>

            <TooltipProvider>
              <Tooltip>
                <TooltipTrigger asChild>
                  <Badge
                    variant={
                      range.color === 'success' ? 'success' :
                      range.color === 'processing' ? 'default' :
                      range.color === 'warning' ? 'warning' : 'destructive'
                    }
                  >
                    {range.text} Range
                  </Badge>
                </TooltipTrigger>
                <TooltipContent>
                  <p>Size range</p>
                </TooltipContent>
              </Tooltip>
            </TooltipProvider>
          </div>
        </div>
      </CardHeader>
      <CardContent>
        <div className="grid gap-6 md:grid-cols-5">
          <div className="md:col-span-3">
            <DataTable
              columns={columns}
              data={data}
            />
          </div>
          <div className="md:col-span-2">
            <Card>
              <CardContent className="pt-6">
                <div className="text-center">
                  <p className="text-sm text-muted-foreground">Size Distribution Score</p>
                  <TooltipProvider>
                    <Tooltip>
                      <TooltipTrigger asChild>
                        <div className="flex items-center justify-center gap-2 mt-2">
                          <Activity className="h-5 w-5" />
                          <span
                            className="text-3xl font-bold"
                            style={{
                              color:
                                quality.color === 'success' ? 'rgb(34 197 94)' :
                                quality.color === 'processing' ? 'rgb(59 130 246)' :
                                quality.color === 'warning' ? 'rgb(234 179 8)' : 'rgb(239 68 68)',
                            }}
                          >
                            {Math.max(0, 100 - (span * 20))}%
                          </span>
                        </div>
                      </TooltipTrigger>
                      <TooltipContent>
                        <p>Overall quality score based on span and range</p>
                      </TooltipContent>
                    </Tooltip>
                  </TooltipProvider>
                </div>

                <div className="mt-4 text-center">
                  <TooltipProvider>
                    <Tooltip>
                      <TooltipTrigger asChild>
                        <Badge
                          variant={
                            range.color === 'success' ? 'success' :
                            range.color === 'processing' ? 'default' :
                            range.color === 'warning' ? 'warning' : 'destructive'
                          }
                        >
                          Range: {(d90 - d10).toFixed(1)} μm
                        </Badge>
                      </TooltipTrigger>
                      <TooltipContent>
                        <p>Ideal range: D90-D10 less than 100μm</p>
                      </TooltipContent>
                    </Tooltip>
                  </TooltipProvider>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </CardContent>
    </Card>
  );
} 