"use client";

import { useQuery } from "@tanstack/react-query";
import {
  ScatterChart,
  Scatter,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  ZAxis,
} from "recharts";
import apiClient from "@/lib/api/client";
import { TooltipProps } from "recharts";
import {
  NameType,
  ValueType,
} from "recharts/types/component/DefaultTooltipContent";

interface EcoEfficiencyData {
  score: {
    current: number;
    previous: number;
    change: number;
  };
  metrics: {
    processId: string;
    environmentalImpact: number;
    economicValue: number;
    efficiency: number;
    timestamp: string;
  }[];
  benchmarks: {
    industry: number;
    target: number;
  };
}

export function EcoEfficiencyDisplay() {
  const { data, isLoading, error } = useQuery<EcoEfficiencyData>({
    queryKey: ["eco-efficiency"],
    queryFn: () => apiClient.get("/api/analysis/environmental/efficiency"),
  });

  if (isLoading)
    return <div className="h-[500px] animate-pulse bg-gray-100 rounded-lg" />;
  if (error)
    return (
      <div className="text-red-500">Error loading eco-efficiency data</div>
    );

  return (
    <div className="space-y-6">
      {/* Efficiency Score Card */}
      <div className="grid grid-cols-3 gap-4">
        <div className="bg-white rounded-lg p-4 shadow-sm">
          <div className="text-sm text-gray-600">Eco-Efficiency Score</div>
          <div className="text-3xl font-bold text-emerald-600">
            {data?.score.current.toFixed(1)}
          </div>
          <div
            className={`text-sm ${
              (data?.score?.change ?? 0) > 0 ? "text-green-600" : "text-red-600"
            }`}
          >
            {(data?.score?.change ?? 0) > 0 ? "↑" : "↓"}{" "}
            {Math.abs(data?.score?.change ?? 0)}%
          </div>
        </div>

        <div className="bg-white rounded-lg p-4 shadow-sm">
          <div className="text-sm text-gray-600">Industry Benchmark</div>
          <div className="text-3xl font-bold text-gray-700">
            {data?.benchmarks.industry.toFixed(1)}
          </div>
          <div className="text-sm text-gray-500">Average Score</div>
        </div>

        <div className="bg-white rounded-lg p-4 shadow-sm">
          <div className="text-sm text-gray-600">Target Score</div>
          <div className="text-3xl font-bold text-blue-600">
            {data?.benchmarks.target.toFixed(1)}
          </div>
          <div className="text-sm text-gray-500">2024 Goal</div>
        </div>
      </div>

      {/* Eco-Efficiency Matrix */}
      <div className="bg-white rounded-lg p-6 shadow-sm">
        <h3 className="text-lg font-semibold mb-4">Eco-Efficiency Matrix</h3>
        <div className="h-[400px]">
          <ResponsiveContainer width="100%" height="100%">
            <ScatterChart margin={{ top: 20, right: 20, bottom: 20, left: 20 }}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis
                type="number"
                dataKey="environmentalImpact"
                name="Environmental Impact"
                label={{ value: "Environmental Impact", position: "bottom" }}
              />
              <YAxis
                type="number"
                dataKey="economicValue"
                name="Economic Value"
                label={{
                  value: "Economic Value (USD)",
                  angle: -90,
                  position: "insideLeft",
                }}
              />
              <ZAxis type="number" dataKey="efficiency" range={[50, 400]} />
              <Tooltip
                cursor={{ strokeDasharray: "3 3" }}
                content={CustomTooltip}
              />
              <Scatter data={data?.metrics} fill="#10B981" />
            </ScatterChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Efficiency Trends */}
      <div className="bg-white rounded-lg p-4 shadow-sm">
        <h3 className="text-lg font-semibold mb-2">Performance Analysis</h3>
        <div className="text-sm text-gray-600">
          <p>
            Current eco-efficiency score is
            {(data?.score?.current ?? 0) > (data?.benchmarks?.industry ?? 0)
              ? " above "
              : " below "}
            industry average by{" "}
            {Math.abs(
              (data?.score?.current ?? 0) - (data?.benchmarks?.industry ?? 0)
            ).toFixed(1)}{" "}
            points.
          </p>
          <p className="mt-2">
            {(data?.score?.current ?? 0) >= (data?.benchmarks?.target ?? 0)
              ? "Target achievement: Met or exceeded"
              : `Gap to target: ${(
                  (data?.benchmarks?.target ?? 0) - (data?.score?.current ?? 0)
                ).toFixed(1)} points`}
          </p>
        </div>
      </div>
    </div>
  );
}

function CustomTooltip({ active, payload }: TooltipProps<ValueType, NameType>) {
  if (!active || !payload?.length) return null;

  return (
    <div className="bg-white p-3 shadow-lg rounded-lg border">
      <p className="text-sm font-medium">Process Analysis</p>
      <p className="text-sm text-gray-600">
        Environmental Impact: {payload[0].value}
      </p>
      <p className="text-sm text-gray-600">
        Economic Value: ${payload[1].value}
      </p>
      <p className="text-sm text-gray-600">
        Efficiency Score: {payload[2].value}
      </p>
    </div>
  );
}
