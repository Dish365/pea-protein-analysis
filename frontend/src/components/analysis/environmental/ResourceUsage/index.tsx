"use client";

import { useQuery } from "@tanstack/react-query";
import {
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  LineChart,
  Line,
} from "recharts";
import apiClient from "@/lib/api/client";

interface ResourceData {
  summary: {
    water: {
      current: number;
      target: number;
      unit: string;
      trend: number;
    };
    energy: {
      current: number;
      target: number;
      unit: string;
      trend: number;
    };
    waste: {
      current: number;
      target: number;
      unit: string;
      trend: number;
    };
  };
  timeline: {
    timestamp: string;
    water: number;
    energy: number;
    waste: number;
  }[];
  efficiency: {
    waterPerUnit: number;
    energyPerUnit: number;
    wastePerUnit: number;
  };
}

export function ResourceUsage() {
  const { data, isLoading, error } = useQuery<ResourceData>({
    queryKey: ["resource-usage"],
    queryFn: () => apiClient.get("/api/analysis/environmental/resources"),
  });

  if (isLoading)
    return <div className="h-[500px] animate-pulse bg-gray-100 rounded-lg" />;
  if (error)
    return (
      <div className="text-red-500">Error loading resource usage data</div>
    );

  return (
    <div className="space-y-6">
      {/* Resource Summary Cards */}
      <div className="grid grid-cols-3 gap-4">
        <ResourceCard
          title="Water Usage"
          current={data?.summary.water.current}
          target={data?.summary.water.target}
          unit={data?.summary.water.unit}
          trend={data?.summary.water.trend}
        />
        <ResourceCard
          title="Energy Consumption"
          current={data?.summary.energy.current}
          target={data?.summary.energy.target}
          unit={data?.summary.energy.unit}
          trend={data?.summary.energy.trend}
        />
        <ResourceCard
          title="Waste Generation"
          current={data?.summary.waste.current}
          target={data?.summary.waste.target}
          unit={data?.summary.waste.unit}
          trend={data?.summary.waste.trend}
        />
      </div>

      {/* Resource Usage Timeline */}
      <div className="bg-white rounded-lg p-6 shadow-sm">
        <h3 className="text-lg font-semibold mb-4">Resource Usage Trends</h3>
        <div className="h-[300px]">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={data?.timeline}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis
                dataKey="timestamp"
                tickFormatter={(value) => new Date(value).toLocaleDateString()}
              />
              <YAxis />
              <Tooltip
                labelFormatter={(value) => new Date(value).toLocaleString()}
                formatter={(value: number, name: string) => [
                  `${value} ${
                    name === "water" ? "m³" : name === "energy" ? "kWh" : "kg"
                  }`,
                  name.charAt(0).toUpperCase() + name.slice(1),
                ]}
              />
              <Line
                type="monotone"
                dataKey="water"
                stroke="#3B82F6"
                strokeWidth={2}
                dot={false}
              />
              <Line
                type="monotone"
                dataKey="energy"
                stroke="#10B981"
                strokeWidth={2}
                dot={false}
              />
              <Line
                type="monotone"
                dataKey="waste"
                stroke="#EF4444"
                strokeWidth={2}
                dot={false}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Resource Efficiency Metrics */}
      <div className="grid grid-cols-3 gap-4">
        <EfficiencyCard
          title="Water Efficiency"
          value={data?.efficiency.waterPerUnit}
          unit="m³/unit"
        />
        <EfficiencyCard
          title="Energy Efficiency"
          value={data?.efficiency.energyPerUnit}
          unit="kWh/unit"
        />
        <EfficiencyCard
          title="Waste Efficiency"
          value={data?.efficiency.wastePerUnit}
          unit="kg/unit"
        />
      </div>
    </div>
  );
}

interface ResourceCardProps {
  title: string;
  current?: number;
  target?: number;
  unit?: string;
  trend?: number;
}

function ResourceCard({
  title,
  current,
  target,
  unit,
  trend,
}: ResourceCardProps) {
  return (
    <div className="bg-white rounded-lg p-4 shadow-sm">
      <div className="text-sm text-gray-600">{title}</div>
      <div className="mt-2">
        <div className="text-2xl font-bold">
          {current} {unit}
        </div>
        <div className="text-sm text-gray-500">
          Target: {target} {unit}
        </div>
      </div>
      {trend && (
        <div
          className={`text-sm mt-2 ${
            trend < 0 ? "text-green-600" : "text-red-600"
          }`}
        >
          {trend < 0 ? "↓" : "↑"} {Math.abs(trend)}% vs last period
        </div>
      )}
      <div className="mt-2 h-2 bg-gray-100 rounded-full">
        <div
          className={`h-full rounded-full ${
            current && target && current <= target
              ? "bg-green-600"
              : "bg-red-600"
          }`}
          style={{
            width: `${
              current && target ? ((current / target) * 100).toFixed(1) : 0
            }%`,
          }}
        />
      </div>
    </div>
  );
}

interface EfficiencyCardProps {
  title: string;
  value?: number;
  unit: string;
}

function EfficiencyCard({ title, value, unit }: EfficiencyCardProps) {
  return (
    <div className="bg-white rounded-lg p-4 shadow-sm">
      <div className="text-sm text-gray-600">{title}</div>
      <div className="text-2xl font-bold mt-2">
        {value?.toFixed(2)} {unit}
      </div>
      <div className="text-sm text-gray-500">Per Production Unit</div>
    </div>
  );
}
