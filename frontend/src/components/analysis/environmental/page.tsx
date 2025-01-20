import { Suspense } from 'react';
import { ImpactMetrics } from '@/components/analysis/environmental/ImpactMetrics';
import { EcoEfficiencyDisplay } from '@/components/analysis/environmental/EcoEfficiencyDisplay';
import { ResourceUsage } from '@/components/analysis/environmental/ResourceUsage';

export default function EnvironmentalAnalysisPage() {
  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Environmental Impact Analysis</h1>
      
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-lg font-semibold mb-4">Environmental Impact</h2>
          <Suspense fallback={<ChartSkeleton />}>
            <ImpactMetrics />
          </Suspense>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-lg font-semibold mb-4">Eco-efficiency Analysis</h2>
          <Suspense fallback={<ChartSkeleton />}>
            <EcoEfficiencyDisplay />
          </Suspense>
        </div>

        <div className="lg:col-span-2 bg-white rounded-lg shadow p-6">
          <h2 className="text-lg font-semibold mb-4">Resource Utilization</h2>
          <Suspense fallback={<ChartSkeleton />}>
            <ResourceUsage />
          </Suspense>
        </div>
      </div>
    </div>
  );
}

function ChartSkeleton() {
  return <div className="h-[300px] bg-gray-100 animate-pulse rounded-lg" />;
}