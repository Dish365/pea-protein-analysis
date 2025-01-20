'use client';

import { useQuery } from '@tanstack/react-query';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, ReferenceLine } from 'recharts';
import { apiClient } from '@/lib/api/client';

interface SensitivityData {
  variables: {
    name: string;
    impact: number;
    scenarios: {
      change: number;
      value: number;
    }[];
  }[];
  baselineNPV: number;
  criticalPoints: {
    variable: string;
    value: number;
    impact: number;
  }[];
}

export function SensitivityAnalysis() {
  const { data, isLoading, error } = useQuery<SensitivityData>({
    queryKey: ['sensitivity-analysis'],
    queryFn: () => apiClient.get('/api/analysis/economic/sensitivity'),
  });

  if (isLoading) return <div className="h-[500px] animate-pulse bg-gray-100 rounded-lg" />;
  if (error) return <div className="text-red-500">Error loading sensitivity analysis data</div>;

  // Sort variables by absolute impact
  const sortedVariables = [...(data?.variables || [])].sort(
    (a, b) => Math.abs(b.impact) - Math.abs(a.impact)
  );

  return (
    <div className="space-y-6">
      {/* Tornado Chart */}
      <div className="bg-white rounded-lg p-6 shadow-sm">
        <h3 className="text-lg font-semibold mb-4">Impact Analysis (Tornado Chart)</h3>
        <div className="h-[400px]">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart
              data={sortedVariables}
              layout="vertical"
              margin={{ top: 20, right: 30, left: 100, bottom: 5 }}
            >
              <XAxis type="number" domain={['dataMin', 'dataMax']} />
              <YAxis dataKey="name" type="category" />
              <Tooltip
                formatter={(value: number) => [`${value.toFixed(2)}%`, 'Impact on NPV']}
              />
              <ReferenceLine x={0} stroke="#666" />
              <Bar
                dataKey="impact"
                fill={(entry) => (entry.impact >= 0 ? '#10B981' : '#EF4444')}
              />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Critical Points */}
      <div className="grid grid-cols-2 gap-4">
        {data?.criticalPoints.map((point) => (
          <div key={point.variable} className="bg-white rounded-lg p-4 shadow-sm">
            <div className="text-sm text-gray-600">{point.variable}</div>
            <div className="text-xl font-bold mt-1">
              {point.value.toFixed(2)}
            </div>
            <div className="text-sm text-gray-500">
              Impact: {point.impact.toFixed(2)}% on NPV
            </div>
          </div>
        ))}
      </div>

      {/* Scenario Analysis */}
      <div className="bg-white rounded-lg p-6 shadow-sm">
        <h3 className="text-lg font-semibold mb-4">Scenario Analysis</h3>
        <div className="space-y-6">
          {sortedVariables.map((variable) => (
            <ScenarioChart
              key={variable.name}
              variable={variable}
              baselineNPV={data?.baselineNPV || 0}
            />
          ))}
        </div>
      </div>

      {/* Analysis Summary */}
      <div className="bg-white rounded-lg p-4 shadow-sm">
        <h3 className="text-lg font-semibold mb-2">Key Insights</h3>
        <div className="text-sm text-gray-600 space-y-2">
          <p>
            Most sensitive variable: {sortedVariables[0]?.name} with 
            {Math.abs(sortedVariables[0]?.impact)}% impact on NPV
          </p>
          <p>
            Baseline NPV: ${data?.baselineNPV.toLocaleString()}
          </p>
          <p>
            Critical threshold: {data?.criticalPoints[0]?.variable} at
            {data?.criticalPoints[0]?.value.toFixed(2)}
          </p>
        </div>
      </div>
    </div>
  );
}

interface ScenarioChartProps {
  variable: {
    name: string;
    scenarios: {
      change: number;
      value: number;
    }[];
  };
  baselineNPV: number;
}

function ScenarioChart({ variable, baselineNPV }: ScenarioChartProps) {
  return (
    <div className="space-y-2">
      <div className="text-sm font-medium">{variable.name}</div>
      <div className="h-[100px]">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={variable.scenarios}>
            <XAxis 
              dataKey="change"
              tickFormatter={(value) => `${value}%`}
            />
            <YAxis 
              domain={['auto', 'auto']}
              tickFormatter={(value) => `$${(value / 1000000).toFixed(1)}M`}
            />
            <Tooltip
              formatter={(value: number) => [
                `$${(value / 1000000).toFixed(2)}M`,
                'NPV'
              ]}
              labelFormatter={(value) => `${value}% Change`}
            />
            <ReferenceLine y={baselineNPV} stroke="#666" strokeDasharray="3 3" />
            <Line
              type="monotone"
              dataKey="value"
              stroke="#6366F1"
              dot={false}
              strokeWidth={2}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}