"use client";

import { useQuery } from "@tanstack/react-query";
import {
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  Line,
  ComposedChart,
  ReferenceLine,
} from "recharts";
import apiClient from "@/lib/api/client";

interface ParticleSizeData {
  distribution: {
    size: number;
    frequency: number;
    cumulative: number;
  }[];
  metrics: {
    d10: number;
    d50: number;
    d90: number;
    meanSize: number;
    standardDev: number;
  };
  targetRange: {
    min: number;
    max: number;
  };
}

export function ParticleSizeDisplay() {
  const { data, isLoading, error } = useQuery<ParticleSizeData>({
    queryKey: ["particle-size"],
    queryFn: () => apiClient.get("/api/analysis/technical/particle-size"),
  });

  if (isLoading)
    return <div className="h-[400px] animate-pulse bg-gray-100 rounded-lg" />;
  if (error)
    return <div className="text-red-500">Error loading particle size data</div>;

  const isWithinTarget = (size: number) => {
    return size >= data!.targetRange.min && size <= data!.targetRange.max;
  };

  return (
    <div className="space-y-6">
      {/* Key Metrics */}
      <div className="grid grid-cols-5 gap-4">
        <MetricCard
          label="D10"
          value={data?.metrics.d10}
          unit="μm"
          status={isWithinTarget(data?.metrics.d10 || 0)}
        />
        <MetricCard
          label="D50 (Median)"
          value={data?.metrics.d50}
          unit="μm"
          status={isWithinTarget(data?.metrics.d50 || 0)}
        />
        <MetricCard
          label="D90"
          value={data?.metrics.d90}
          unit="μm"
          status={isWithinTarget(data?.metrics.d90 || 0)}
        />
        <MetricCard
          label="Mean Size"
          value={data?.metrics.meanSize}
          unit="μm"
          status={isWithinTarget(data?.metrics.meanSize || 0)}
        />
        <MetricCard
          label="Std Dev"
          value={data?.metrics.standardDev}
          unit="μm"
          status="neutral"
        />
      </div>

      {/* Distribution Chart */}
      <div className="bg-white rounded-lg p-4 shadow-sm">
        <h3 className="text-lg font-semibold mb-4">
          Particle Size Distribution
        </h3>
        <div className="h-[400px]">
          <ResponsiveContainer width="100%" height="100%">
            <ComposedChart data={data?.distribution}>
              <XAxis
                dataKey="size"
                label={{ value: "Particle Size (μm)", position: "bottom" }}
              />
              <YAxis
                yAxisId="left"
                label={{
                  value: "Frequency (%)",
                  angle: -90,
                  position: "insideLeft",
                }}
              />
              <YAxis
                yAxisId="right"
                orientation="right"
                label={{
                  value: "Cumulative (%)",
                  angle: 90,
                  position: "insideRight",
                }}
              />
              <Tooltip
                formatter={(value: number, name: string) => [
                  `${value.toFixed(2)}%`,
                  name === "frequency" ? "Frequency" : "Cumulative",
                ]}
              />
              <Bar
                yAxisId="left"
                dataKey="frequency"
                fill="#4F46E5"
                opacity={0.8}
                name="Frequency"
              />
              <Line
                yAxisId="right"
                type="monotone"
                dataKey="cumulative"
                stroke="#EF4444"
                strokeWidth={2}
                name="Cumulative"
              />
              {/* Target Range Markers */}
              <ReferenceLine
                x={data?.targetRange.min}
                stroke="#10B981"
                strokeDasharray="3 3"
                label="Min Target"
              />
              <ReferenceLine
                x={data?.targetRange.max}
                stroke="#10B981"
                strokeDasharray="3 3"
                label="Max Target"
              />
            </ComposedChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Analysis Summary */}
      <div className="bg-white rounded-lg p-4 shadow-sm">
        <h3 className="text-lg font-semibold mb-2">Distribution Analysis</h3>
        <div className="text-sm text-gray-600">
          <p>
            The particle size distribution shows a
            {(data?.metrics?.d50 ?? 0) >
            ((data?.targetRange?.max ?? 0) + (data?.targetRange?.min ?? 0)) / 2
              ? "right-skewed"
              : "left-skewed"}
            pattern with a median size of {data?.metrics.d50}μm.
          </p>
          <p className="mt-2">
            {(data?.metrics?.d90 ?? 0) - (data?.metrics?.d10 ?? 0)}μm span
            between D10 and D90 indicates a
            {((data?.metrics?.d90 ?? 0) - (data?.metrics?.d10 ?? 0)) /
              (data?.metrics?.d50 ?? 1) >
            2
              ? " wide "
              : " narrow "}
            distribution range.
          </p>
        </div>
      </div>
    </div>
  );
}

interface MetricCardProps {
  label: string;
  value?: number;
  unit: string;
  status: boolean | "neutral";
}

function MetricCard({ label, value, unit, status }: MetricCardProps) {
  const getStatusColor = () => {
    if (status === "neutral") return "text-gray-600";
    return status ? "text-green-600" : "text-red-600";
  };

  return (
    <div className="bg-white rounded-lg p-4 shadow-sm">
      <div className="text-sm text-gray-600">{label}</div>
      <div className={`text-xl font-bold ${getStatusColor()}`}>
        {value?.toFixed(1)} {unit}
      </div>
    </div>
  );
}
