'use client';

import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Legend } from 'recharts';
import { useProcess } from '@/lib/hooks/useProcess';

interface CostData {
  category: string;
  capex: number;
  opex: number;
  total: number;
}

export function CostBreakdown() {
  const { data, isLoading, error } = useProcess('cost-breakdown');

  if (isLoading) return <div className="h-[400px] animate-pulse bg-gray-100 rounded-lg" />;
  if (error) return <div className="text-red-500">Error loading cost data</div>;

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-3 gap-4">
        <CostMetricCard
          label="Total CAPEX"
          value={data?.totalCapex}
          currency="USD"
        />
        <CostMetricCard
          label="Annual OPEX"
          value={data?.annualOpex}
          currency="USD"
        />
        <CostMetricCard
          label="Unit Cost"
          value={data?.unitCost}
          currency="USD/kg"
        />
      </div>

      <ResponsiveContainer width="100%" height={400}>
        <BarChart data={data?.costBreakdown}>
          <XAxis dataKey="category" />
          <YAxis />
          <Tooltip 
            formatter={(value: number) => [`$${value.toLocaleString()}`, 'Cost']}
          />
          <Legend />
          <Bar dataKey="capex" name="CAPEX" fill="#4F46E5" />
          <Bar dataKey="opex" name="OPEX" fill="#10B981" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}

interface CostMetricCardProps {
  label: string;
  value: number;
  currency: string;
}

function CostMetricCard({ label, value, currency }: CostMetricCardProps) {
  const formattedValue = currency === 'USD' 
    ? `$${value.toLocaleString()}`
    : `${value.toLocaleString()} ${currency}`;

  return (
    <div className="bg-gray-50 rounded-lg p-4">
      <div className="text-sm text-gray-600">{label}</div>
      <div className="text-xl font-semibold mt-1">{formattedValue}</div>
    </div>
  );
}