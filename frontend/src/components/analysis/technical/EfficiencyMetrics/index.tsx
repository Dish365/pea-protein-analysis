'use client';

import { useQuery } from '@tanstack/react-query';
import { RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar, ResponsiveContainer, Tooltip } from 'recharts';
import { apiClient } from '@/lib/api/client';

interface EfficiencyData {
  currentEfficiency: number;
  historicalEfficiency: number;
  metrics: {
    name: string;
    current: number;
    baseline: number;
  }[];
  trends: {
    timestamp: string;
    efficiency: number;
  }[];
}

export function EfficiencyMetrics() {
  const { data, isLoading, error } = useQuery<EfficiencyData>({
    queryKey: ['efficiency-metrics'],
    queryFn: () => apiClient.get('/api/analysis/technical/efficiency'),
  });

  if (isLoading) return <div className="h-[400px] animate-pulse bg-gray-100 rounded-lg" />;
  if (error) return <div className="text-red-500">Error loading efficiency metrics</div>;

  return (
    <div className="space-y-6">
      {/* Efficiency Score Card */}
      <div className="grid grid-cols-2 gap-4">
        <div className="bg-white rounded-lg p-4 shadow-sm">
          <div className="text-sm text-gray-600">Current Efficiency</div>
          <div className="text-3xl font-bold text-indigo-600">
            {data?.currentEfficiency}%
          </div>
          <div className={`text-sm ${
            data?.currentEfficiency > data?.historicalEfficiency 
              ? 'text-green-600' 
              : 'text-red-600'
          }`}>
            {data?.currentEfficiency > data?.historicalEfficiency ? '↑' : '↓'}
            {Math.abs(data?.currentEfficiency - data?.historicalEfficiency)}% vs historical
          </div>
        </div>

        <div className="bg-white rounded-lg p-4 shadow-sm">
          <div className="text-sm text-gray-600">Key Metrics</div>
          <div className="mt-2 space-y-2">
            {data?.metrics.slice(0, 3).map((metric) => (
              <div key={metric.name} className="flex justify-between items-center">
                <span className="text-sm">{metric.name}</span>
                <span className="text-sm font-semibold">{metric.current}%</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Radar Chart for Multiple Metrics */}
      <div className="bg-white rounded-lg p-4 shadow-sm">
        <h3 className="text-lg font-semibold mb-4">Efficiency Breakdown</h3>
        <div className="h-[300px]">
          <ResponsiveContainer width="100%" height="100%">
            <RadarChart data={data?.metrics}>
              <PolarGrid />
              <PolarAngleAxis dataKey="name" />
              <PolarRadiusAxis angle={30} domain={[0, 100]} />
              <Radar
                name="Current"
                dataKey="current"
                stroke="#4F46E5"
                fill="#4F46E5"
                fillOpacity={0.3}
              />
              <Radar
                name="Baseline"
                dataKey="baseline"
                stroke="#94A3B8"
                fill="#94A3B8"
                fillOpacity={0.3}
              />
              <Tooltip />
            </RadarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Efficiency Metrics Details */}
      <div className="grid grid-cols-2 gap-4">
        {data?.metrics.map((metric) => (
          <MetricCard
            key={metric.name}
            name={metric.name}
            current={metric.current}
            baseline={metric.baseline}
          />
        ))}
      </div>
    </div>
  );
}

interface MetricCardProps {
  name: string;
  current: number;
  baseline: number;
}

function MetricCard({ name, current, baseline }: MetricCardProps) {
  const improvement = current - baseline;
  
  return (
    <div className="bg-white rounded-lg p-4 shadow-sm">
      <div className="text-sm font-medium text-gray-600">{name}</div>
      <div className="mt-2 flex justify-between items-end">
        <div>
          <div className="text-2xl font-bold">{current}%</div>
          <div className="text-sm text-gray-500">Current</div>
        </div>
        <div className={`text-sm ${improvement >= 0 ? 'text-green-600' : 'text-red-600'}`}>
          {improvement >= 0 ? '+' : ''}{improvement}%
          <div className="text-gray-500">vs Baseline</div>
        </div>
      </div>
      <div className="mt-2 h-2 bg-gray-100 rounded-full overflow-hidden">
        <div 
          className="h-full bg-indigo-600 rounded-full"
          style={{ width: `${current}%` }}
        />
      </div>
    </div>
  );
}