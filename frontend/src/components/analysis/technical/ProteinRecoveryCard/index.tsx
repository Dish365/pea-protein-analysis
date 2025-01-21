"use client";

import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
} from "recharts";
import { useProcess } from "@/lib/hooks/useProcess";

interface TimeSeriesData {
  timestamp: string;
  recovery: number;
  target: number;
}

export interface ProcessData {
  currentRecovery: number;
  improvement: number;
  timeSeriesData: TimeSeriesData[];
  peakRecovery: number;
  peakTrend: { value: number; direction: "up" | "down" };
  averageRate: number;
  avgTrend: { value: number; direction: "up" | "down" };
  processTime: number;
  timeTrend: { value: number; direction: "up" | "down" };
}

export function ProteinRecoveryChart() {
  const { data, isLoading, error } = useProcess("protein-recovery");

  if (isLoading)
    return <div className="h-[300px] animate-pulse bg-gray-100 rounded-lg" />;
  if (error)
    return (
      <div className="text-red-500">Error loading protein recovery data</div>
    );

  return (
    <div className="space-y-4">
      <div className="flex justify-between items-center">
        <div>
          <div className="text-2xl font-bold">
            {data?.data?.currentRecovery}%
          </div>
          <div className="text-sm text-gray-600">Current Recovery Rate</div>
        </div>
        <div className="text-right">
          <div className="text-lg font-semibold text-green-600">
            +{data?.data?.improvement}%
          </div>
          <div className="text-sm text-gray-600">vs Baseline</div>
        </div>
      </div>

      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={data?.data?.timeSeriesData}>
          <XAxis
            dataKey="timestamp"
            tickFormatter={(value) => new Date(value).toLocaleTimeString()}
          />
          <YAxis domain={[0, 100]} />
          <Tooltip
            formatter={(value: number) => [`${value}%`, "Recovery Rate"]}
            labelFormatter={(label) => new Date(label).toLocaleString()}
          />
          <Line
            type="monotone"
            dataKey="recovery"
            stroke="#4F46E5"
            strokeWidth={2}
          />
          <Line
            type="monotone"
            dataKey="target"
            stroke="#E5E7EB"
            strokeDasharray="5 5"
          />
        </LineChart>
      </ResponsiveContainer>

      <div className="grid grid-cols-3 gap-4 mt-4">
        <MetricCard
          label="Peak Recovery"
          value={`${data?.data?.peakRecovery}%`}
          trend={data?.data?.peakTrend}
        />
        <MetricCard
          label="Average Rate"
          value={`${data?.data?.averageRate}%`}
          trend={data?.data?.avgTrend}
        />
        <MetricCard
          label="Process Time"
          value={`${data?.data?.processTime}min`}
          trend={data?.data?.timeTrend}
        />
      </div>
    </div>
  );
}

interface MetricCardProps {
  label: string;
  value: string;
  trend?: {
    value: number;
    direction: "up" | "down";
  };
}

function MetricCard({ label, value, trend }: MetricCardProps) {
  return (
    <div className="bg-gray-50 rounded-lg p-3">
      <div className="text-sm text-gray-600">{label}</div>
      <div className="text-lg font-semibold">{value}</div>
      {trend && (
        <div
          className={`text-sm ${
            trend.direction === "up" ? "text-green-600" : "text-red-600"
          }`}
        >
          {trend.direction === "up" ? "↑" : "↓"} {trend.value}%
        </div>
      )}
    </div>
  );
}
