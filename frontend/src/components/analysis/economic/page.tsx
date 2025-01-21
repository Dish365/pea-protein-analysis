import { Suspense } from 'react';
import { CostBreakdown } from '@/components/analysis/economic/CostBreakdown';
import { ProfitabilityMetrics } from '@/components/analysis/economic/ProfitabilityMetrics';
import { SensitivityAnalysis } from '@/components/analysis/economic/SensitivityAnalysis';

export default function EconomicAnalysisPage() {
  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Economic Analysis Dashboard</h1>
      
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 bg-white rounded-lg shadow p-6">
          <h2 className="text-lg font-semibold mb-4">Cost Analysis</h2>
          <Suspense fallback={<ChartSkeleton />}>
            <CostBreakdown />
          </Suspense>
        </div>

        <div className="space-y-6">
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-lg font-semibold mb-4">Key Metrics</h2>
            <Suspense fallback={<MetricsSkeleton />}>
              <ProfitabilityMetrics />
            </Suspense>
          </div>
        </div>

        <div className="lg:col-span-3 bg-white rounded-lg shadow p-6">
          <h2 className="text-lg font-semibold mb-4">Sensitivity Analysis</h2>
          <Suspense fallback={<ChartSkeleton />}>
            <SensitivityAnalysis />
          </Suspense>
        </div>
      </div>
    </div>
  );
}

function ChartSkeleton() {
  return <div className="h-[300px] bg-gray-100 animate-pulse rounded-lg" />;
}

function MetricsSkeleton() {
  return (
    <div className="space-y-4">
      {[1, 2, 3].map((i) => (
        <div key={i} className="h-8 bg-gray-100 animate-pulse rounded" />
      ))}
    </div>
  );
}