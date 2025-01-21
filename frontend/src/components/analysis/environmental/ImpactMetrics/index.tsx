"use client";

import { useQuery } from "@tanstack/react-query";
import {
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  Radar,
  ResponsiveContainer,
  Tooltip,
} from "recharts";
import apiClient from "@/lib/api/client";

interface ImpactData {
  metrics: {
    category: string;
    value: number;
    benchmark: number;
  }[];
  totalScore: {
    current: number;
    previous: number;
    change: number;
  };
  carbonFootprint: {
    value: number;
    unit: string;
    reduction: number;
  };
}

export function ImpactMetrics() {
  const { data, isLoading, error } = useQuery<ImpactData>({
    queryKey: ["environmental-impact"],
    queryFn: () => apiClient.get("/api/analysis/environmental/impact"),
  });

  if (isLoading)
    return <div className="h-[400px] animate-pulse bg-gray-100 rounded-lg" />;
  if (error)
    return (
      <div className="text-red-500">
        Error loading environmental impact data
      </div>
    );

  return (
    <div className="space-y-6">
      {/* Impact Score Overview */}
      <div className="grid grid-cols-2 gap-4">
        <div className="bg-white rounded-lg p-4 shadow-sm">
          <div className="text-sm text-gray-600">
            Environmental Impact Score
          </div>
          <div className="text-3xl font-bold text-green-600">
            {data?.totalScore.current}
          </div>
          <div
            className={`text-sm ${
              (data?.totalScore?.change ?? 0) >= 0
                ? "text-red-600"
                : "text-green-600"
            }`}
          >
            {(data?.totalScore?.change ?? 0) >= 0 ? "↑" : "↓"}
            {Math.abs(data?.totalScore?.change ?? 0)}% vs previous
          </div>
        </div>

        <div className="bg-white rounded-lg p-4 shadow-sm">
          <div className="text-sm text-gray-600">Carbon Footprint</div>
          <div className="text-3xl font-bold text-gray-800">
            {data?.carbonFootprint.value}
            <span className="text-sm ml-1">{data?.carbonFootprint.unit}</span>
          </div>
          <div className="text-sm text-green-600">
            ↓ {data?.carbonFootprint.reduction}% reduction
          </div>
        </div>
      </div>

      {/* Impact Categories Radar Chart */}
      <div className="h-[300px]">
        <ResponsiveContainer width="100%" height="100%">
          <RadarChart data={data?.metrics}>
            <PolarGrid />
            <PolarAngleAxis dataKey="category" />
            <Tooltip />
            <Radar
              name="Current Impact"
              dataKey="value"
              stroke="#10B981"
              fill="#10B981"
              fillOpacity={0.3}
            />
            <Radar
              name="Industry Benchmark"
              dataKey="benchmark"
              stroke="#94A3B8"
              fill="#94A3B8"
              fillOpacity={0.3}
            />
          </RadarChart>
        </ResponsiveContainer>
      </div>

      {/* Detailed Metrics */}
      <div className="grid grid-cols-2 gap-4">
        {data?.metrics.map((metric) => (
          <ImpactMetricCard
            key={metric.category}
            category={metric.category}
            value={metric.value}
            benchmark={metric.benchmark}
          />
        ))}
      </div>
    </div>
  );
}

interface ImpactMetricCardProps {
  category: string;
  value: number;
  benchmark: number;
}

function ImpactMetricCard({
  category,
  value,
  benchmark,
}: ImpactMetricCardProps) {
  const performance = ((benchmark - value) / benchmark) * 100;

  return (
    <div className="bg-white rounded-lg p-4 shadow-sm">
      <div className="text-sm font-medium text-gray-600">{category}</div>
      <div className="mt-2 flex justify-between items-end">
        <div>
          <div className="text-2xl font-bold">{value}</div>
          <div className="text-sm text-gray-500">Current Impact</div>
        </div>
        <div
          className={`text-sm ${
            performance >= 0 ? "text-green-600" : "text-red-600"
          }`}
        >
          {performance >= 0 ? "↓" : "↑"} {Math.abs(performance).toFixed(1)}%
          <div className="text-gray-500">vs Benchmark</div>
        </div>
      </div>
      <div className="mt-2 h-2 bg-gray-100 rounded-full overflow-hidden">
        <div
          className={`h-full ${
            performance >= 0 ? "bg-green-600" : "bg-red-600"
          }`}
          style={{ width: `${Math.min(Math.abs(performance), 100)}%` }}
        />
      </div>
    </div>
  );
}
