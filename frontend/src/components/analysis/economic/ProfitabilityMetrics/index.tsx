'use client';

import { useQuery } from '@tanstack/react-query';
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';
import { apiClient } from '@/lib/api/client';

interface ProfitabilityData {
  metrics: {
    roi: number;
    paybackPeriod: number;
    npv: number;
    irr: number;
    profitMargin: number;
  };
  trends: {
    timestamp: string;
    revenue: number;
    costs: number;
    profit: number;
  }[];
  comparison: {
    current: number;
    previous: number;
    change: number;
  };
}

export function ProfitabilityMetrics() {
  const { data, isLoading, error } = useQuery<ProfitabilityData>({
    queryKey: ['profitability-metrics'],
    queryFn: () => apiClient.get('/api/analysis/economic/profitability'),
  });

  if (isLoading) return <div className="h-[400px] animate-pulse bg-gray-100 rounded-lg" />;
  if (error) return <div className="text-red-500">Error loading profitability data</div>;

  return (
    <div className="space-y-6">
      {/* Key Metrics Grid */}
      <div className="grid grid-cols-2 gap-4">
        <MetricCard
          label="ROI"
          value={data?.metrics.roi}
          format="percentage"
          trend={data?.comparison}
        />
        <MetricCard
          label="Payback Period"
          value={data?.metrics.paybackPeriod}
          format="years"
          trend={data?.comparison}
        />
        <MetricCard
          label="NPV"
          value={data?.metrics.npv}
          format="currency"
          trend={data?.comparison}
        />
        <MetricCard
          label="IRR"
          value={data?.metrics.irr}
          format="percentage"
          trend={data?.comparison}
        />
      </div>

      {/* Profit Margin Indicator */}
      <div className="bg-white rounded-lg p-4 shadow-sm">
        <div className="flex justify-between items-center mb-2">
          <div className="text-sm text-gray-600">Profit Margin</div>
          <div className="text-lg font-bold">
            {data?.metrics.profitMargin.toFixed(1)}%
          </div>
        </div>
        <div className="h-2 bg-gray-100 rounded-full">
          <div
            className="h-full bg-green-600 rounded-full"
            style={{ width: `${Math.max(0, Math.min(100, data?.metrics.profitMargin || 0))}%` }}
          />
        </div>
      </div>

      {/* Revenue vs Costs Trend */}
      <div className="bg-white rounded-lg p-4 shadow-sm">
        <h3 className="text-lg font-semibold mb-4">Financial Performance Trend</h3>
        <div className="h-[200px]">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={data?.trends}>
              <XAxis 
                dataKey="timestamp"
                tickFormatter={(value) => new Date(value).toLocaleDateString()}
              />
              <YAxis />
              <Tooltip
                formatter={(value: number) => [`$${value.toLocaleString()}`, '']}
                labelFormatter={(label) => new Date(label).toLocaleDateString()}
              />
              <Line
                type="monotone"
                dataKey="revenue"
                stroke="#10B981"
                name="Revenue"
                strokeWidth={2}
              />
              <Line
                type="monotone"
                dataKey="costs"
                stroke="#EF4444"
                name="Costs"
                strokeWidth={2}
              />
              <Line
                type="monotone"
                dataKey="profit"
                stroke="#6366F1"
                name="Profit"
                strokeWidth={2}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}

interface MetricCardProps {
  label: string;
  value?: number;
  format: 'percentage' | 'currency' | 'years';
  trend?: {
    current: number;
    previous: number;
    change: number;
  };
}

function MetricCard({ label, value, format, trend }: MetricCardProps) {
  const formatValue = (val?: number) => {
    if (val === undefined) return '-';
    switch (format) {
      case 'percentage':
        return `${val.toFixed(1)}%`;
      case 'currency':
        return `$${val.toLocaleString()}`;
      case 'years':
        return `${val.toFixed(1)} years`;
      default:
        return val.toString();
    }
  };

  return (
    <div className="bg-white rounded-lg p-4 shadow-sm">
      <div className="text-sm text-gray-600">{label}</div>
      <div className="text-2xl font-bold mt-1">
        {formatValue(value)}
      </div>
      {trend && (
        <div className={`text-sm mt-1 ${
          trend.change >= 0 ? 'text-green-600' : 'text-red-600'
        }`}>
          {trend.change >= 0 ? '↑' : '↓'} {Math.abs(trend.change)}%
        </div>
      )}
    </div>
  );
}